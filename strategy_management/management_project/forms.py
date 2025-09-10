from django import forms
from .models import *
from management_project.services.vision import VisionService
from management_project.services.mission import MissionService


class OrganizationalProfileForm(forms.ModelForm):

    class Meta:

        model = OrganizationalProfile

        fields = [
            'organization_name', 'organization_address', 'employer_tin', 'organization_type',
            'sector_name', 'contact_personnel'
        ]

        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization Name'
            }),
            'organization_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization Address'
            }),
            'employer_tin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Employer TIN'
            }),

            'organization_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sector_name': forms.Select(attrs={
                'class': 'form-control',
            }),
            'contact_personnel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Personnel'
            }),
        }


class StakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        # Exclude automatically set or relationship fields
        exclude = [
            'priority', 'contribution_score', 'depends_on',
        ]

        widgets = {
            'organization_name': forms.Select(attrs={'class': 'form-control'}),
            'stakeholder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stakeholder Name'}),
            'stakeholder_type': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department or Team'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description'}),
            'impact_level': forms.Select(attrs={'class': 'form-control'}),
            'interest_level': forms.Select(attrs={'class': 'form-control'}),
            'engagement_strategy': forms.Select(attrs={'class': 'form-control'}),
            'influence_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Influence Score'}),
            'satisfaction_level': forms.Select(attrs={'class': 'form-control'}),
            'risk_level': forms.Select(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email, Phone, or Contact'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Format help texts with inline CSS
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'

        # Add 'is-invalid' class to fields with errors
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs.update({'class': 'form-control is-invalid'})

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'



class PayrollPeriodForm(forms.ModelForm):

    class Meta:
        model = PayrollPeriod
        fields = [
            'year', 'month',

        ]
        widgets = {
            'year': forms.Select(choices=YEAR_CHOICES),
            'month': forms.Select(choices=MONTH_CHOICES),
            **{field.name: forms.CheckboxInput(attrs={'class': 'form-check-input'})
               for field in model._meta.get_fields()
               if isinstance(field, models.BooleanField)}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Adding the Bootstrap 'form-select' class to the year and month select fields
        self.fields['year'].widget.attrs.update({'class': 'form-select'})
        self.fields['month'].widget.attrs.update({'class': 'form-select'})

        # Add inline CSS to the help text
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'



class PayrollMonthComponentForm(forms.ModelForm):

    class Meta:
        model = PayrollMonthComponent
        fields = [
            'payroll_month',
            'use_basic_salary', 'use_overtime', 'use_housing_allowance', 'use_position_allowance',
            'use_commission', 'use_telephone_allowance', 'use_one_time_bonus', 'use_causal_labor_wage',
            'use_transport_home_to_office', 'use_transport_for_work', 'use_fuel_home_to_office',
            'use_fuel_for_work', 'use_per_diem', 'use_hardship_allowance', 'use_public_cash_award',
            'use_incidental_operation_allowance', 'use_medical_allowance',
            'use_cash_gift', 'use_tuition_fees', 'use_personal_injury',
            'use_child_support_payment', 'use_charitable_donation', 'use_saving_plan', 'use_loan_payment',
            'use_court_order', 'use_workers_association', 'use_personnel_insurance_saving',
            'use_university_cost_share_pay', 'use_red_cross', 'use_party_contribution', 'use_other_deduction'
        ]
        widgets = {
            'payroll_month': forms.Select(attrs={'class': 'form-control'}),
             #
            **{field.name: forms.CheckboxInput(attrs={'class': 'form-check-input'})
               for field in model._meta.get_fields()
               if isinstance(field, models.BooleanField)}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Adding the Bootstrap 'form-select' class to the year and month select fields
        self.fields['payroll_month'].widget.attrs.update({'class': 'form-select'})

        # Add inline CSS to the help text
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'


class RegularPayrollForm(forms.ModelForm):
    processing_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RegularPayroll
        exclude = [

            'organization_name', 'personnel_id', 'first_name', 'father_name', 'last_name', 'employment_type', 'phone_number', 'city', 'pension_number',
            'position_name', 'working_area', 'personnel_tin', 'working_environment', 'overtime', 'transport_home_to_office_taxable',
            'transport_home_to_office_non_taxable', 'fuel_home_to_office_taxable', 'fuel_home_to_office_non_taxable',
            'transport_for_work_taxable', 'transport_for_work_non_taxable', 'fuel_for_work_taxable',
            'fuel_for_work_non_taxable',
            'per_diem_taxable', 'per_diem_non_taxable',
            'hardship_allowance_taxable', 'hardship_allowance_non_taxable', 'employee_pension_contribution',
            'employer_pension_contribution', 'total_pension_contribution', 'employment_income_tax',
            #cost share
            'university_cost_share_pay',
            # Totals
            'total_payroll_deduction', 'gross_pay', 'gross_taxable_pay', 'gross_non_taxable_pay', 'net_pay',
            'total_payroll_deduction', 'expense',
            #

            'bank_name', 'bank_account_id', 'bank_account_type'
        ]

        widgets = {
            'personnel_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stakeholder_list ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'personnel_full_name': forms.Select(attrs={'class': 'form-control'}),

            'employment_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employment type'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'position_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter position name'}),
            'working_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter position type'}),
            'pension_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pension number'}),
            'personnel_tin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stakeholder_list TIN'}),
            'working_environment': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter working environment'}),
            'payroll_month': forms.Select(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter basic salary'}),
            'overtime_hours_from_six_pm_to_four_pm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter overtime'}),
            'overtime_hours_from_four_pm_to_six_am': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter overtime'}),
            'overtime_hours_in_weekly_rest_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter overtime'}),
            'overtime_hours_in_public_holiday': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter overtime'}),

            'housing_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter housing allowance'}),
            'position_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter position allowance'}),
            'commission': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter commission'}),
            'telephone_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter telephone allowance'}),
            'one_time_bonus': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter one-time bonus'}),
            'causal_labor_wage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter causal labor wage'}),
            'transport_home_to_office': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter transport allowance for home to office'}),
            'fuel_home_to_office': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter fuel allowance for home to office'}),
            'transport_for_work': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter transport allowance for work'}),
            'fuel_for_work': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter fuel allowance for work'}),
            'per_diem': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total per diem with in a month'}),
            'hardship_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter hardship allowance'}),
            'public_cash_award': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter public cash award'}),
            'incidental_operation_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter incidental operation allowance'}),
            'medical_allowance': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter medical allowance'}),
            'cash_gift': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter cash gift'}),
            'tuition_fees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter tuition fees'}),
            'personal_injury': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter personal injury'}),
            'child_support_payment': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter child support payment'}),
            #
            #
            'charitable_donation': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter charitable donation'}),
            'saving_plan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter saving plan'}),
            'loan_payment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter loan payment'}),
            'court_order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter court order'}),
            'workers_association': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter workers association'}),
            'personnel_insurance_saving': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter stakeholder_list insurance saving'}),
            'cost_share_percent_to_basic_salary': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cost share percent to basic salary'}),
            'university_cost_share_pay': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter university cost share pay'}),
            'red_cross': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter red cross'}),
            'party_contribution': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter party contribution'}),
            'other_deduction': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter other deduction'}),
             #
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bank name'}),
            'bank_account_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bank account ID'}),
            'bank_account_type': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter bank account type'}),
            'processing_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Select pay day', 'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


        # Filter personnels by current user
        if self.request and self.request.user.is_authenticated and hasattr(self.request.user, 'organization_name'):
            self.fields['personnel_full_name'].queryset = Stakeholder.objects.filter(
                organization_name=self.request.user.organization_name)
            self.fields['payroll_month'].queryset = PayrollMonthComponent.objects.filter(
                organization_name=self.request.user.organization_name)

        else:
            self.fields['personnel_full_name'].queryset = Stakeholder.objects.none()
            self.fields['payroll_month'].queryset = PayrollMonthComponent.objects.none()


        # Get payroll_month from initial data or instance
        payroll_month = self.initial.get('payroll_month') or self.instance.payroll_month
        
        if isinstance(payroll_month, int):
            try:
                payroll_month = PayrollMonthComponent.objects.get(id=payroll_month)
            except PayrollMonthComponent.DoesNotExist:
                payroll_month = None

        # Conditionally hide fields based on payroll_month options
        if payroll_month:
            if not payroll_month.use_basic_salary:
                self.fields['basic_salary'].widget = forms.HiddenInput()

            if not payroll_month.use_overtime:
                self.fields['overtime_hours_from_six_pm_to_four_pm'].widget = forms.HiddenInput()
                self.fields['overtime_hours_from_four_pm_to_six_am'].widget = forms.HiddenInput()
                self.fields['overtime_hours_in_weekly_rest_day'].widget = forms.HiddenInput()
                self.fields['overtime_hours_in_public_holiday'].widget = forms.HiddenInput()

            if not payroll_month.use_transport_home_to_office:
                self.fields['transport_home_to_office'].widget = forms.HiddenInput()

            if not payroll_month.use_fuel_home_to_office:
                self.fields['fuel_home_to_office'].widget = forms.HiddenInput()

            if not payroll_month.use_transport_for_work:
                self.fields['transport_for_work'].widget = forms.HiddenInput()

            if not payroll_month.use_fuel_for_work:
                self.fields['fuel_for_work'].widget = forms.HiddenInput()

            if not payroll_month.use_per_diem:
                self.fields['per_diem'].widget = forms.HiddenInput()

            if not payroll_month.use_hardship_allowance:
                self.fields['hardship_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_housing_allowance:
                self.fields['housing_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_position_allowance:
                self.fields['position_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_commission:
                self.fields['commission'].widget = forms.HiddenInput()

            if not payroll_month.use_telephone_allowance:
                self.fields['telephone_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_one_time_bonus:
                self.fields['one_time_bonus'].widget = forms.HiddenInput()

            if not payroll_month.use_causal_labor_wage:
                self.fields['causal_labor_wage'].widget = forms.HiddenInput()

            if not payroll_month.use_public_cash_award:
                self.fields['public_cash_award'].widget = forms.HiddenInput()

            if not payroll_month.use_incidental_operation_allowance:
                self.fields['incidental_operation_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_medical_allowance:
                self.fields['medical_allowance'].widget = forms.HiddenInput()

            if not payroll_month.use_cash_gift:
                self.fields['cash_gift'].widget = forms.HiddenInput()

            if not payroll_month.use_tuition_fees:
                self.fields['tuition_fees'].widget = forms.HiddenInput()

            if not payroll_month.use_personal_injury:
                self.fields['personal_injury'].widget = forms.HiddenInput()

            if not payroll_month.use_child_support_payment:
                self.fields['child_support_payment'].widget = forms.HiddenInput()

            if not payroll_month.use_charitable_donation:
                self.fields['charitable_donation'].widget = forms.HiddenInput()

            if not payroll_month.use_saving_plan:
                self.fields['saving_plan'].widget = forms.HiddenInput()

            if not payroll_month.use_loan_payment:
                self.fields['loan_payment'].widget = forms.HiddenInput()

            if not payroll_month.use_court_order:
                self.fields['court_order'].widget = forms.HiddenInput()

            if not payroll_month.use_workers_association:
                self.fields['workers_association'].widget = forms.HiddenInput()

            if not payroll_month.use_personnel_insurance_saving:
                self.fields['personnel_insurance_saving'].widget = forms.HiddenInput()

            if not payroll_month.use_university_cost_share_pay:
                # self.fields['university_cost_share_pay'].widget = forms.HiddenInput()
                self.fields['cost_share_percent_to_basic_salary'].widget = forms.HiddenInput()

            if not payroll_month.use_red_cross:
                self.fields['red_cross'].widget = forms.HiddenInput()

            if not payroll_month.use_party_contribution:
                self.fields['party_contribution'].widget = forms.HiddenInput()
                
            if not payroll_month.use_other_deduction:
                self.fields['other_deduction'].widget = forms.HiddenInput()
                # Set default widget attributes like placeholders for fields that remain visible

        # Add inline CSS to the help text
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'
        # Add 'is-invalid' color class to fields with errors
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs.update({'class': 'form-control is-invalid'})
        # Automatically apply the CSS class to fields with errors

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'




#earning adjustment
class EarningAdjustmentForm(forms.ModelForm):

    payroll_to_record = forms.ModelChoiceField(
        queryset=RegularPayroll.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    payroll_needing_adjustment = forms.ModelChoiceField(
        queryset=RegularPayroll.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    class Meta:

        model = EarningAdjustment

        fields = [
            'payroll_to_record', 'payroll_needing_adjustment', 'case', 'component', 'earning_amount',
            'period_start', 'period_end', 'months_covered',
        ]

        widgets = {
            'payroll_to_record': forms.Select(attrs={'class': 'form-control'}),
            'payroll_needing_adjustment': forms.Select(attrs={'class': 'form-control', 'Placeholder': 'Processing Month'}),
            'case': forms.Select(attrs={'class': 'form-control'}),
            'component': forms.Select(attrs={'class': 'form-control'}),
            'earning_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'months_covered': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['payroll_to_record'].help_text = "The current payroll month where you're recording the adjustment."
        self.fields[
            'payroll_needing_adjustment'].help_text = "The past payroll month that had an issue, missed pay, or error."
        #
        # Check if the request exists, the user is authenticated, and the user has an organization assigned

        if (
                self.request
                and self.request.user.is_authenticated
                and hasattr(self.request.user, 'organization_name')
                and self.request.user.organization_name
        ):
            org = self.request.user.organization_name
            self.fields['payroll_needing_adjustment'].queryset = RegularPayroll.objects.filter(
                organization_name=org
            )
            self.fields['payroll_to_record'].queryset = RegularPayroll.objects.filter(
                organization_name=org
            )
        else:
            self.fields['payroll_needing_adjustment'].queryset = RegularPayroll.objects.none()
            self.fields['payroll_to_record'].queryset = RegularPayroll.objects.none()



#deduction adjustment

class DeductionAdjustmentForm(forms.ModelForm):
    payroll_to_record = forms.ModelChoiceField(
        queryset=RegularPayroll.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    payroll_needing_adjustment = forms.ModelChoiceField(
        queryset=RegularPayroll.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    class Meta:

        model = DeductionAdjustment

        fields = [
            'payroll_to_record', 'payroll_needing_adjustment',
            'case', 'component', 'deduction_amount', 'period_start',
            'period_end', 'months_covered', 'created_at', 'updated_at',
        ]

        widgets = {
            'payroll_to_record': forms.Select(attrs={'class': 'form-select'}),
            'payroll_needing_adjustment': forms.Select(attrs={'class': 'form-select'}),
            'case': forms.Select(attrs={'class': 'form-select'}),
            'component': forms.Select(attrs={'class': 'form-select'}),
            'deduction_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'period_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'months_covered': forms.NumberInput(attrs={'class': 'form-control'}),
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'updated_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['payroll_to_record'].help_text = "The current payroll month where you're recording the adjustment."
        self.fields[
            'payroll_needing_adjustment'].help_text = "The past payroll month that had an issue, missed pay, or error."
        #
        # Check if the request exists, the user is authenticated, and the user has an organization assigned

        if (
                self.request
                and self.request.user.is_authenticated
                and hasattr(self.request.user, 'organization_name')
                and self.request.user.organization_name
        ):
            org = self.request.user.organization_name
            self.fields['payroll_needing_adjustment'].queryset = RegularPayroll.objects.filter(
                organization_name=org
            )
            self.fields['payroll_to_record'].queryset = RegularPayroll.objects.filter(
                organization_name=org
            )
        else:
            self.fields['payroll_needing_adjustment'].queryset = RegularPayroll.objects.none()
            self.fields['payroll_to_record'].queryset = RegularPayroll.objects.none()


#severance pay

class SeverancePayForm(forms.ModelForm):
    class Meta:
        model = SeverancePay
        exclude = [
            'organization_name', 'personnel_id', 'first_name', 'father_name', 'last_name',
            'service_years', 'service_days', 'severance_for_years', 'severance_for_days', 'gross_severance_pay',
            'basic_salary', 'prorate_salary', 'employment_income_tax_from_basic_salary',
            'total_employment_income_tax_from_basic_salary',
            'employment_income_tax_from_prorate_salary', 'employment_income_tax_from_severance_pay', 'net_severance_pay',
        ]
        widgets = {
            'severance_record_month': forms.Select(choices=MONTH_CHOICES),
            'personnel_full_name': forms.Select(attrs={'class': 'form-control'}),
            'severance_type': forms.Select(attrs={'class': 'form-control'}),

            'last_week_daily_wages': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter last week daily wages'}),
            'start_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Select service start date', 'type': 'date'}),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Select service end date', 'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SeverancePayForm, self).__init__(*args, **kwargs)

        # Filter personnels by current user
        if self.request and self.request.user.is_authenticated and hasattr(self.request.user, 'organization_name'):
            self.fields['personnel_full_name'].queryset = Stakeholder.objects.filter(organization_name = self.request.user.organization_name)
        else:
            self.fields['personnel_full_name'].queryset = Stakeholder.objects.none()

        self.fields['severance_record_month'].widget.attrs.update({'class': 'form-select'})

        # Add inline CSS to the help text
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'
        # Add 'is-invalid' color class to fields with errors
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs.update({'class': 'form-control is-invalid'})
        # Automatically apply the CSS class to fields with errors

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'


class VisionForm(forms.ModelForm):
    class Meta:
        model = Vision
        fields = ['organization_name', 'vision_statement',]
        widgets = {
            'organization_name': forms.HiddenInput(),  # Hide the field
            'vision_statement': forms.Select(attrs={'class': 'form-control'}),
        }

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Safe default organization
        default_org = getattr(self.instance, 'organization_name', None) or OrganizationalProfile.objects.first()

        # Override with GET/POST data if available
        org_id = None
        if self.request:
            org_id = self.request.GET.get('organization_id') or self.data.get('organization_name')
        if org_id:
            default_org = OrganizationalProfile.objects.filter(id=org_id).first() or default_org

        self.fields['organization_name'].initial = default_org

        # Use VisionService instance
        self.service = VisionService(default_org)

        # Set vision statement choices
        vision_choices = self.service.get_choices()
        if vision_choices:
            self.fields['vision_statement'].widget.choices = vision_choices
            self.fields['vision_statement'].initial = getattr(self.instance, 'vision_statement', None) or vision_choices[0][0]
        else:
            self.fields['vision_statement'].widget.attrs['disabled'] = True

        # Add error class for invalid fields
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs['class'] = f"{field.widget.attrs.get('class', '')} is-invalid"

    def clean(self):
        cleaned_data = super().clean()
        vision_statement = cleaned_data.get('vision_statement')
        if vision_statement:
            try:
                self.service.validate_choice(vision_statement)
            except ValueError as e:
                self.add_error('vision_statement', str(e))
        return cleaned_data


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['organization_name', 'mission_statement']
        widgets = {
            'organization_name': forms.HiddenInput(),  # Hide the field
            'mission_statement': forms.Select(attrs={'class': 'form-control'}),
        }

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Safe default organization
        default_org = getattr(self.instance, 'organization_name', None) or OrganizationalProfile.objects.first()

        # Override with GET/POST data if available
        org_id = None
        if self.request:
            org_id = self.request.GET.get('organization_id') or self.data.get('organization_name')
        if org_id:
            default_org = OrganizationalProfile.objects.filter(id=org_id).first() or default_org

        self.fields['organization_name'].initial = default_org

        # Use MissionService instance
        self.service = MissionService(default_org)

        # Set mission statement choices
        mission_choices = self.service.get_choices()
        if mission_choices:
            self.fields['mission_statement'].widget.choices = mission_choices
            self.fields['mission_statement'].initial = getattr(self.instance, 'mission_statement', None) or mission_choices[0][0]
        else:
            self.fields['mission_statement'].widget.attrs['disabled'] = True

        # Add error class for invalid fields
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs['class'] = f"{field.widget.attrs.get('class', '')} is-invalid"

    def clean(self):
        cleaned_data = super().clean()
        mission_statement = cleaned_data.get('mission_statement')
        if mission_statement:
            try:
                self.service.validate_choice(mission_statement)
            except ValueError as e:
                self.add_error('mission_statement', str(e))
        return cleaned_data