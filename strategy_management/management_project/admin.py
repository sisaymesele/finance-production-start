from django.contrib import admin
from .models import OrganizationalProfile, Stakeholder, PayrollPeriod, PayrollMonthComponent, RegularPayroll, EarningAdjustment, \
    SeverancePay, Vision
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
# config/admin.py
import management_project.config.admin


# Register your models here.
@admin.register(OrganizationalProfile)
class OrganizationalProfileAdmin(admin.ModelAdmin):
    # form = OrganizationalProfileForm
    list_display = (
        'organization_name', 'organization_type', 'organization_address', 'employer_tin',
        'sector_name', 'contact_personnel',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    form = StakeholderForm

    # Fields to display in the list view
    list_display = (
        'organization_name', 'stakeholder_name', 'role', 'department',
        'stakeholder_type', 'impact_level', 'interest_level', 'engagement_strategy',
        'priority', 'satisfaction_level', 'risk_level', 'influence_score'
    )

    # Fields to exclude from the admin form
    exclude = ('priority', 'contribution_score', 'depends_on')

    # Fields that can be searched
    search_fields = ('stakeholder_name', 'organization_name__organization_name', 'department')

    # Filtering options in admin sidebar
    list_filter = ('stakeholder_type', 'role', 'impact_level', 'interest_level', 'satisfaction_level', 'risk_level')

    # Auto-filter based on user's organization (if not superuser)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs["queryset"] = OrganizationalProfile.objects.filter(pk=org.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Limit queryset for non-superusers to their organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()


@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):

    list_display = [
        'organization_name', 'year', 'month', 'payroll_month',
    ]
    list_filter = ['year', 'month']

    # Explicitly get the form to ensure custom widgets are used
    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = PayrollPeriodForm
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        # This method is new in Django 5+ and allows passing custom kwargs to the form
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()



@admin.register(PayrollMonthComponent)
class PayrollMonthComponentAdmin(admin.ModelAdmin):
    # form = PayrollMonthComponentForm
    list_display = [
        'organization_name', 'payroll_month',
        'use_basic_salary', 'use_overtime', 'use_housing_allowance', 'use_position_allowance',
        'use_commission', 'use_telephone_allowance', 'use_one_time_bonus', 'use_causal_labor_wage',
        # partial taxable
        'use_transport_home_to_office', 'use_transport_for_work', 'use_fuel_home_to_office',
        'use_fuel_for_work', 'use_per_diem', 'use_hardship_allowance', 'use_public_cash_award',
        'use_incidental_operation_allowance', 'use_medical_allowance',
        'use_cash_gift', 'use_tuition_fees', 'use_personal_injury',
        'use_child_support_payment',
        # deduction
        'use_charitable_donation', 'use_saving_plan',
        'use_loan_payment', 'use_court_order', 'use_workers_association', 'use_personnel_insurance_saving',
        'use_university_cost_share_pay', 'use_red_cross', 'use_party_contribution', 'use_other_deduction', 'slug',
    ]
    list_filter = ['payroll_month']

    # Group fields by their categories for better organization
    fieldsets = (
        ('Payroll Month', {
            'fields': ('organization_name', 'payroll_month')
        }),
        ('Fully Taxable Components', {
            'fields': (
                'use_basic_salary', 'use_overtime',
                'use_housing_allowance', 'use_position_allowance',
                'use_commission', 'use_telephone_allowance',
                'use_one_time_bonus', 'use_causal_labor_wage'
            )
        }),
        ('Partially Taxable Components', {
            'fields': (
                'use_transport_home_to_office', 'use_transport_for_work',
                'use_fuel_home_to_office', 'use_fuel_for_work',
                'use_per_diem', 'use_hardship_allowance'
            )
        }),
        ('Fully Non-Taxable Compensation', {
            'fields': (
                'use_public_cash_award', 'use_incidental_operation_allowance',
                'use_medical_allowance', 'use_cash_gift', 'use_tuition_fees',
                'use_personal_injury', 'use_child_support_payment',
            )
        }),
        ('Deductions', {
            'fields': (
                'use_charitable_donation', 'use_saving_plan', 'use_loan_payment',
                'use_court_order', 'use_workers_association',
                'use_personnel_insurance_saving', 'use_university_cost_share_pay',
                'use_red_cross', 'use_party_contribution', 'use_other_deduction'
            )
        }),
    )

    # Explicitly get the form to ensure custom widgets are used
    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = PayrollMonthComponentForm
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        # This method is new in Django 5+ and allows passing custom kwargs to the form
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()


# #
@admin.register(RegularPayroll)
class RegularPayrollAdmin(admin.ModelAdmin):
    list_display = [
        'organization_name', 'get_personnel_id', 'get_first_name', 'get_father_name', 'get_last_name',
        #
        'payroll_month', 'basic_salary',
        'overtime', 'housing_allowance', 'position_allowance', 'commission', 'telephone_allowance',
        'one_time_bonus', 'causal_labor_wage',
        #
        'transport_home_to_office', 'transport_home_to_office_taxable', 'transport_home_to_office_non_taxable',
        'fuel_home_to_office', 'fuel_home_to_office_taxable', 'fuel_home_to_office_non_taxable',
        'transport_for_work', 'transport_for_work_taxable', 'transport_for_work_non_taxable',
        'fuel_for_work', 'fuel_for_work_taxable', 'fuel_for_work_non_taxable',
        'per_diem', 'per_diem_taxable', 'per_diem_non_taxable', 'per_diem', 'per_diem_taxable',
        'per_diem_non_taxable', 'hardship_allowance', 'hardship_allowance_taxable', 'hardship_allowance_non_taxable',
        #
        'public_cash_award', 'incidental_operation_allowance', 'medical_allowance', 'cash_gift', 'tuition_fees',
        'personal_injury', 'child_support_payment',
        # deduction
        # conditional deduction
        'charitable_donation', 'saving_plan', 'loan_payment', 'court_order', 'workers_association',
        'personnel_insurance_saving', 'cost_share_percent_to_basic_salary', 'university_cost_share_pay',
        'red_cross', 'party_contribution', 'other_deduction',
        # auto deduction
        'employment_income_tax', 'employee_pension_contribution',
        'employer_pension_contribution', 'total_pension_contribution',
        # summary
        'total_payroll_deduction', 'gross_pay', 'gross_taxable_pay',
        'gross_non_taxable_pay', 'net_pay', 'expense',
    ]
    list_filter = ['payroll_month__payroll_month__month', 'payroll_month__payroll_month__year', 'organization_name']

    @admin.display(ordering='personnel_full_name__personnel_id', description='Personnel ID')
    def get_personnel_id(self, obj):
        return obj.personnel_full_name.personnel_id

    @admin.display(ordering='personnel_full_name__first_name', description='First Name')
    def get_first_name(self, obj):
        return obj.personnel_full_name.first_name

    @admin.display(ordering='personnel_full_name__father_name', description='Father Name')
    def get_father_name(self, obj):
        return obj.personnel_full_name.father_name

    @admin.display(ordering='personnel_full_name__last_name', description='Last Name')
    def get_last_name(self, obj):
        return obj.personnel_full_name.last_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)
            if db_field.name == 'personnel_full_name':
                kwargs["queryset"] = Stakeholder.objects.filter(organization_name=org)
            if db_field.name == 'payroll_month':
                kwargs["queryset"] = PayrollMonthComponent.objects.filter(organization_name=org)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        # This method is new in Django 5+ and allows passing custom kwargs to the form
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()


# # earning adjustment admin
@admin.register(EarningAdjustment)
class EarningAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'organization_name', 'get_personnel_id', 'get_first_name', 'get_father_name', 'get_last_name',
        'case', 'component', 'earning_amount', 'period_start', 'period_end', 'months_covered',
        'taxable', 'non_taxable', 'adjusted_month_total_earning_deduction',
        #
        'adjusted_month_employee_pension_contribution',
        'adjusted_month_employer_pension_contribution',
        'adjusted_month_total_pension',
        #
        'recorded_month_taxable_gross_pay', 'recorded_month_non_taxable_gross_pay',
        'recorded_month_gross_pay', 'recorded_month_total_taxable_pay',
        'recorded_month_employment_income_tax_total', 'recorded_month_employment_income_tax',
        #
        'recorded_month_employee_pension_contribution',
        'recorded_month_employer_pension_contribution',
        'recorded_month_total_pension_contribution',
        #
        'recorded_month_total_earning_deduction', 'recorded_month_expense'

    )

    list_filter = ('component', 'payroll_to_record', 'payroll_needing_adjustment',)
    search_fields = ('component', 'payroll_to_record', 'payroll_needing_adjustment',)
    ordering = ('-created_at',)

    readonly_fields = (
        'taxable', 'non_taxable', 'adjusted_month_gross_taxable_pay',
        'adjusted_month_gross_non_taxable_pay', 'adjusted_month_gross_pay',
        'adjusted_month_total_taxable_pay', 'adjusted_month_employment_income_tax_total',
        'adjusted_month_employment_income_tax', 'adjusted_month_total_earning_deduction',
        'adjusted_month_expense', 'recorded_month_taxable_gross_pay',
        'recorded_month_non_taxable_gross_pay', 'recorded_month_gross_pay',
        'recorded_month_total_taxable_pay', 'recorded_month_employment_income_tax_total',
        'recorded_month_employment_income_tax', 'recorded_month_total_earning_deduction',
        'recorded_month_expense', 'created_at', 'updated_at',
    )

    # Group fields into logical sections

    @admin.display(ordering='payroll_to_record__personnel_full_name__personnel_id', description='Personnel ID')
    def get_personnel_id(self, obj):
        return obj.payroll_to_record.personnel_full_name.personnel_id

    @admin.display(ordering='payroll_to_record__personnel_full_name__first_name', description='First Name')
    def get_first_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.first_name

    @admin.display(ordering='payroll_to_record__personnel_full_name__father_name', description='Father Name')
    def get_father_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.father_name

    @admin.display(ordering='payroll_to_record__personnel_full_name__last_name', description='Last Name')
    def get_last_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.last_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)
            if db_field.name == 'payroll_to_record':
                kwargs["queryset"] = RegularPayroll.objects.filter(organization_name=org)
            if db_field.name == 'payroll_needing_adjustment':
                kwargs["queryset"] = RegularPayroll.objects.filter(organization_name=org)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        # This method is new in Django 5+ and allows passing custom kwargs to the form
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    #
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()
    #


# deduction adjustment
@admin.register(DeductionAdjustment)
class DeductionAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        'organization_name', 'get_personnel_id', 'get_first_name', 'get_father_name', 'get_last_name',
        'component', 'case', 'deduction_amount', 'adjusted_month_total_deduction',
        'recorded_month_total_deduction', 'months_covered',
        'period_start', 'period_end', 'created_at', 'updated_at',
    )

    list_filter = ('component', 'payroll_to_record', 'payroll_needing_adjustment',)
    search_fields = ('component', 'payroll_to_record', 'payroll_needing_adjustment',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    @admin.display(ordering='payroll_to_record__personnel_full_name__personnel_id', description='Personnel ID')
    def get_personnel_id(self, obj):
        return obj.payroll_to_record.personnel_full_name.personnel_id

    @admin.display(ordering='payroll_to_record__personnel_full_name__first_name', description='First Name')
    def get_first_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.first_name

    @admin.display(ordering='payroll_to_record__personnel_full_name__father_name', description='Father Name')
    def get_father_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.father_name

    @admin.display(ordering='payroll_to_record__personnel_full_name__last_name', description='Last Name')
    def get_last_name(self, obj):
        return obj.payroll_to_record.personnel_full_name.last_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)
            if db_field.name == 'payroll_to_record':
                kwargs["queryset"] = RegularPayroll.objects.filter(organization_name=org)
            if db_field.name == 'payroll_needing_adjustment':
                kwargs["queryset"] = RegularPayroll.objects.filter(organization_name=org)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(
                organization_name=request.user.organization_name
            )
        return qs.none()


# severance pay

@admin.register(SeverancePay)
class SeverancePayAdmin(admin.ModelAdmin):
    list_display = (
        'severance_record_month', 'severance_type', 'get_personnel_id', 'personnel_full_name',
        'get_first_name', 'get_father_name', 'get_last_name',
        'last_week_daily_wages', 'start_date', 'end_date',
        'service_years', 'service_days', 'severance_for_years', 'severance_for_days',
        'gross_severance_pay', 'basic_salary', 'prorate_salary', 'employment_income_tax_from_basic_salary',
        'total_employment_income_tax_from_basic_salary', 'employment_income_tax_from_prorate_salary',
        'employment_income_tax_from_severance_pay', 'net_severance_pay',
    )
    search_fields = ('personnel_full_name__first_name', 'personnel_full_name__last_name')

    @admin.display(ordering='personnel_full_name__personnel_id', description='Personnel ID')
    def get_personnel_id(self, obj):
        return obj.personnel_full_name.personnel_id

    @admin.display(ordering='personnel_full_name__first_name', description='First Name')
    def get_first_name(self, obj):
        return obj.personnel_full_name.first_name

    @admin.display(ordering='personnel_full_name__father_name', description='Father Name')
    def get_father_name(self, obj):
        return obj.personnel_full_name.father_name

    @admin.display(ordering='personnel_full_name__last_name', description='Last Name')
    def get_last_name(self, obj):
        return obj.personnel_full_name.last_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)
            if db_field.name == 'personnel_full_name':
                kwargs["queryset"] = Stakeholder.objects.filter(organization_name=org)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs["request"] = request
        return form_kwargs

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()

@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    form = VisionForm

    # Display these fields in the list view
    list_display = ('organization_name', 'vision_statement')

    # Filter foreign key based on user (non-superuser sees only their organization)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                kwargs["queryset"] = OrganizationalProfile.objects.filter(
                    pk=request.user.organization_name.pk
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Filter the queryset in the admin list view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()