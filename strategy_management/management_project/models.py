from django.db import models
import datetime
from django.core.exceptions import ValidationError
import re
# choices
from .choices.country_code_choices import COUNTRY_CODE_CHOICES
from .choices.payroll_month_choices import YEAR_CHOICES, MONTH_CHOICES
# date and utils
from django.utils.text import slugify
from django.db.models import Sum
# stakeholder_list info
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import MinValueValidator
# services

from .services.regular_payroll import RegularPayrollService
from .services.earning_adjustment.business import EarningAdjustmentBusinessService
from .services.earning_adjustment.context import get_earning_adjustment_context
from .services.deduction_adjustment.business import DeductionAdjustmentBusinessService
from .services.deduction_adjustment.context import get_deduction_adjustment_context
from .services.severance_pay import SeverancePayService
from .services.absence_deduction import VisionService
from management_project.services.pension import calculate_pension_contributions



# Create your models here.
class OrganizationalProfile(models.Model):
    organization_choices = [
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('partnership', 'Partnership'), ('corporation', 'Corporation'),
        ('joint_venture', 'Joint Venture'), ('cooperative', 'Cooperative'), ('non_profit', 'Non Profit'),
        ('non_governmental', 'Non Governmental'), ('governmental', 'Governmental'),
        ('other', 'Other')
    ]
    SECTOR_CHOICES = [
        ('education', 'Education'),
        ('healthcare', 'Healthcare & Medical Services'),
        ('information_technology', 'Information Technology & Digital Services'),
        ('finance_banking', 'Finance, Banking & Insurance'),
        ('agriculture', 'Agriculture & Agribusiness'),
        ('manufacturing', 'Manufacturing & Industry'),
        ('energy_utilities', 'Energy & Utilities'),
        ('environment_sustainability', 'Environment & Sustainability'),
        ('transport_logistics', 'Transportation & Logistics'),
        ('tourism_hospitality', 'Tourism, Travel & Hospitality'),
        ('construction_real_estate', 'Construction & Real Estate'),
        ('telecommunications', 'Telecommunications'),
        ('research_development', 'Research & Development'),
        ('public_sector', 'Government & Public Administration'),
        ('creative_media', 'Creative Arts, Media & Entertainment'),
        ('retail_wholesale', 'Retail & Wholesale Trade'),
        ('ecommerce', 'E-commerce & Online Retail'),
        ('professional_services', 'Professional & Business Services'),
        ('hospitality_food', 'Hospitality & Food Services'),
        ('mining_resources', 'Mining, Oil & Natural Resources'),
    ]
    organization_name = models.CharField(max_length=80, unique=True)
    organization_address = models.CharField(max_length=80)
    employer_tin = models.CharField(max_length=90, verbose_name='Employer TIN')
    organization_type = models.CharField(choices=organization_choices, max_length=70)
    sector_name = models.CharField( max_length=50, choices=SECTOR_CHOICES, unique=True)
    contact_personnel = models.CharField(max_length=90)

    def __str__(self):
        return str(self.organization_name)

    class Meta:
        verbose_name = "Organizational Profile"
        verbose_name_plural = "               Organizational Profile"
        ordering = ['-id']


def validate_phone_number(value):
    # Regular expression pattern to validate phone number without country code
    pattern = r'^\d{9,10}'
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid phone number (7-12 digits) without country code.")


class Stakeholder(models.Model):
    # ------------------ Choices ------------------
    STAKEHOLDER_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('executive', 'Executive'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('team_lead', 'Team Lead'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('qa', 'Quality Assurance'),
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('customer', 'Customer'),
        ('partner', 'Partner'),
        ('supplier', 'Supplier'),
        ('investor', 'Investor'),
        ('regulator', 'Regulator'),
        ('community', 'Community'),
        ('other', 'Other'),
    ]

    IMPACT_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    INTEREST_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    ENGAGEMENT_STRATEGY_CHOICES = [
        ('inform', 'Inform'),
        ('consult', 'Consult'),
        ('involve', 'Involve'),
        ('collaborate', 'Collaborate'),
        ('empower', 'Empower'),
    ]

    SATISFACTION_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # ------------------ Core Info ------------------
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    stakeholder_name = models.CharField(max_length=200, help_text="Stakeholder name or organization")
    stakeholder_type = models.CharField(max_length=20, choices=STAKEHOLDER_TYPE_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True, help_text="Optional department or team")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the stakeholder")

    # ------------------ Analysis ------------------
    impact_level = models.CharField(max_length=20, choices=IMPACT_LEVEL_CHOICES, default='medium')
    interest_level = models.CharField(max_length=20, choices=INTEREST_LEVEL_CHOICES, default='medium')
    engagement_strategy = models.CharField(max_length=20, choices=ENGAGEMENT_STRATEGY_CHOICES, default='inform')
    influence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                          help_text="Quantitative measure of influence")
    priority = models.PositiveIntegerField(default=0, help_text="Calculated from impact x interest x influence")

    satisfaction_level = models.CharField(max_length=20, choices=SATISFACTION_LEVEL_CHOICES, default='medium',
                                          help_text="Stakeholder satisfaction with the project or SaaS")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='medium',
                                  help_text="Potential risk if stakeholder is disengaged")
    contribution_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                             help_text="Estimated contribution to strategic objectives")

    # ------------------ Contact ------------------
    contact_info = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Email, phone, or other contact details")
    notes = models.TextField(blank=True, null=True, help_text="Additional observations or comments")

    # ------------------ Relationships ------------------
    depends_on = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="influences",
        help_text="Other stakeholders this stakeholder depends on or influences"
    )

    class Meta:
        ordering = ["-priority", "stakeholder_name"]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    # ------------------ Business Logic ------------------
    def save(self, *args, **kwargs):
        # Priority calculation: impact * interest * influence (normalized)
        impact_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        interest_map = {'low': 1, 'medium': 2, 'high': 3}
        influence_factor = float(self.influence_score) if self.influence_score else 1.0

        self.priority = int(impact_map.get(self.impact_level, 2) *
                            interest_map.get(self.interest_level, 2) *
                            influence_factor)


        super().save(*args, **kwargs)

    @property
    def is_key_stakeholder(self):
        """High priority stakeholders who need close attention"""
        return self.priority >= 6

    @property
    def risk_score(self):
        """Assign numerical risk based on risk_level"""
        risk_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        return risk_map.get(self.risk_level, 2)

    @property
    def impact_interest_matrix(self):
        """Quick reference for categorization"""
        return f"Impact: {self.impact_level}, Interest: {self.interest_level}"



class PayrollPeriod(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES,
                            default=str(datetime.datetime.now().year),
                            help_text='payroll processing year')
    month = models.CharField(max_length=12, choices=MONTH_CHOICES,
                             default=datetime.datetime.now().strftime('%B'),
                             help_text='payroll processing month')

    payroll_month = models.CharField(max_length=70, blank=True)
    slug = models.SlugField(unique=True)  # Slug for payroll month

    def __str__(self):
        # Defensive: ensure always string
        if isinstance(self.payroll_month, str):
            return self.payroll_month
        return str(self.payroll_month)

    class Meta:
        verbose_name = "              Payroll Month and Component"
        verbose_name_plural = "              Payroll Month and Components"
        ordering = ['-id']  # You can change the ordering field as needed

    def save(self, *args, **kwargs):
        self.payroll_month = f"{self.get_month_display()}-{self.year}"
        if self.organization_name_id:
            self.slug = f"{self.organization_name.id}-{self.payroll_month}"
        else:
            self.slug = self.payroll_month
        super().save(*args, **kwargs)



class PayrollMonthComponent(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    payroll_month = models.ForeignKey(PayrollPeriod, on_delete=models.PROTECT, help_text='payroll processing month')
    use_basic_salary = models.BooleanField(default=False)
    use_overtime = models.BooleanField(default=False)
    use_housing_allowance = models.BooleanField(default=False)
    use_position_allowance = models.BooleanField(default=False)
    use_commission = models.BooleanField(default=False)
    use_telephone_allowance = models.BooleanField(default=False)
    use_one_time_bonus = models.BooleanField(default=False)
    use_causal_labor_wage = models.BooleanField(default=False)
    # partially taxable
    use_transport_home_to_office = models.BooleanField(default=False)
    use_transport_for_work = models.BooleanField(default=False)
    use_fuel_home_to_office = models.BooleanField(default=False)
    use_fuel_for_work = models.BooleanField(default=False)
    use_per_diem = models.BooleanField(default=False)
    use_hardship_allowance = models.BooleanField(default=False)

    # Fully non_taxable compensation
    use_public_cash_award = models.BooleanField(default=False)
    use_incidental_operation_allowance = models.BooleanField(default=False)
    use_medical_allowance = models.BooleanField(default=False)
    use_cash_gift = models.BooleanField(default=False)
    use_tuition_fees = models.BooleanField(default=False)
    use_personal_injury = models.BooleanField(default=False)
    use_child_support_payment = models.BooleanField(default=False)

    # Deductions
    use_charitable_donation = models.BooleanField(default=False)
    use_saving_plan = models.BooleanField(default=False)
    use_loan_payment = models.BooleanField(default=False)
    use_court_order = models.BooleanField(default=False)
    use_workers_association = models.BooleanField(default=False)
    use_personnel_insurance_saving = models.BooleanField(default=False)
    use_university_cost_share_pay = models.BooleanField(default=False)
    use_red_cross = models.BooleanField(default=False)
    use_party_contribution = models.BooleanField(default=False)
    use_other_deduction = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)  # Slug for payroll month

    def __str__(self):
        return str(self.payroll_month)

    class Meta:
        verbose_name = "              Payroll Month and Component"
        verbose_name_plural = "              Payroll Month and Components"
        ordering = ['-id']  # You can change the ordering field as needed

    def save(self, *args, **kwargs):
        if self.organization_name_id:
            self.slug = f"{self.organization_name.id}-{self.payroll_month}"
        else:
            self.slug = self.payroll_month
        super().save(*args, **kwargs)


class RegularPayroll(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    # stakeholder_list information

    personnel_full_name = models.ForeignKey(Stakeholder, on_delete=models.PROTECT, help_text='Please select personnel full name')

    payroll_month = models.ForeignKey(PayrollMonthComponent, on_delete=models.PROTECT, help_text='Payroll processing month')
    # fully taxable compensation
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(Decimal('0.00'))],
                                       help_text='Monthly pay for work done')
    overtime_hours_from_six_pm_to_four_pm = models.IntegerField(blank=True, null=True,
                                                                validators=[MinValueValidator(Decimal('0.00'))],
                                                                help_text='Total over time hour from 6 pm to 4 pm with in a pay month')
    overtime_hours_from_four_pm_to_six_am = models.IntegerField(blank=True, null=True,
                                                                validators=[MinValueValidator(Decimal('0.00'))],
                                                                help_text='Total over time hour from 4 pm to 6 am with in a pay month')
    overtime_hours_in_weekly_rest_day = models.IntegerField(blank=True, null=True,
                                                            validators=[MinValueValidator(Decimal('0.00'))],
                                                            help_text='Total over time hour in weekly rest day - saturday and sunday with in a pay month')
    overtime_hours_in_public_holiday = models.IntegerField(blank=True, null=True,
                                                           validators=[MinValueValidator(Decimal('0.00'))],
                                                           help_text='Total over time hour in public holiday with in a pay month')
    overtime = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(Decimal('0.00'))])
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])
    position_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                             validators=[MinValueValidator(Decimal('0.00'))])
    commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    telephone_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              validators=[MinValueValidator(Decimal('0.00'))])
    one_time_bonus = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                         validators=[MinValueValidator(Decimal('0.00'))])
    causal_labor_wage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])
    # partially taxable compensation
    #
    transport_home_to_office = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                   validators=[MinValueValidator(Decimal('0.00'))],
                                                   help_text='Monthly transport allowance for home to office transport')
    transport_home_to_office_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transport_home_to_office_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    #
    fuel_home_to_office = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              validators=[MinValueValidator(Decimal('0.00'))],
                                              help_text='Monthly fuel allowance for home to office transport')
    fuel_home_to_office_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fuel_home_to_office_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    #
    transport_for_work = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                             validators=[MinValueValidator(Decimal('0.00'))],
                                             help_text='Monthly transport allowance for work purposes')
    transport_for_work_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transport_for_work_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    #
    fuel_for_work = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                        validators=[MinValueValidator(Decimal('0.00'))],
                                        help_text='Monthly fuel allowance for work purposes')
    fuel_for_work_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fuel_for_work_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    #
    per_diem = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                   validators=[MinValueValidator(Decimal('0.00'))],
                                   help_text='Per diem per day or daily per diem')
    per_diem_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    per_diem_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    #
    hardship_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                             validators=[MinValueValidator(Decimal('0.00'))],
                                             help_text='Monthly allowance for working in unfavorable conditions')
    hardship_allowance_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hardship_allowance_non_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # full tax exempt compensation
    public_cash_award = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])
    incidental_operation_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                         validators=[MinValueValidator(Decimal('0.00'))])
    medical_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])
    cash_gift = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                    validators=[MinValueValidator(Decimal('0.00'))])
    tuition_fees = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(Decimal('0.00'))])
    personal_injury = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                          validators=[MinValueValidator(Decimal('0.00'))])
    child_support_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                validators=[MinValueValidator(Decimal('0.00'))])

    # deductions
    # conditional deduction
    charitable_donation = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              validators=[MinValueValidator(Decimal('0.00'))])
    saving_plan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(Decimal('0.00'))])
    loan_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                       validators=[MinValueValidator(Decimal('0.00'))])
    court_order = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(Decimal('0.00'))])
    workers_association = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                              validators=[MinValueValidator(Decimal('0.00'))])
    personnel_insurance_saving = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                     validators=[MinValueValidator(Decimal('0.00'))])
    cost_share_percent_to_basic_salary = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                                             validators=[MinValueValidator(Decimal('0.00'))],
                                                             help_text='Percent of cost share deduction from agreed basic salary with in a month')
    university_cost_share_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                    validators=[MinValueValidator(Decimal('0.00'))])
    red_cross = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                    validators=[MinValueValidator(Decimal('0.00'))])
    party_contribution = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                             validators=[MinValueValidator(Decimal('0.00'))])
    other_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                          validators=[MinValueValidator(Decimal('0.00'))])
    # summary
    # auto deduction
    # tax
    employment_income_tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # pension
    employee_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    employer_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # gross
    gross_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    gross_non_taxable_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    gross_taxable_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_payroll_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    net_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    # bank information
    bank_name = models.CharField(max_length=70, blank=True, null=True)
    bank_account_id = models.CharField(max_length=70, blank=True, null=True)
    bank_account_type = models.CharField(max_length=70, blank=True, null=True)
    processing_date = models.DateField(null=True, blank=True, default=datetime.date.today)


    def __str__(self):
        try:
            payroll = str(self.payroll_month)
        except self.__class__.payroll_month.RelatedObjectDoesNotExist:
            payroll = "No Payroll Month"

        try:
            personnel = str(self.personnel_full_name)  # or .name if you want only the name field
        except self.__class__.personnel_full_name.RelatedObjectDoesNotExist:
            personnel = "No Personnel"

        return f"{payroll} - {personnel}"


    class Meta:
        verbose_name = "             Regular Payroll"
        verbose_name_plural = "             Regular Payroll"
        ordering = ['payroll_month', '-id']  # You can change the ordering field as needed

    def clean(self):
        if self.personnel_full_name:
            # perdiem check
            if self.per_diem and (
                    (not self.personnel_full_name.daily_per_diem or self.personnel_full_name.daily_per_diem == Decimal(
                        '0.00'))
            ):
                raise ValidationError({
                    'per_diem': 'To process per diem you should add daily per diem amount in personnel list.'
                })

            # only one payroll per month for an personnel
            if RegularPayroll.objects.exclude(pk=self.pk).filter(
                    personnel_full_name=self.personnel_full_name,
                    payroll_month=self.payroll_month
            ).exists():
                raise ValidationError({
                    'payroll_month': 'An adjustment for this personnel and month already exists.'
                })

            # hardship check

            allowed_environments = ['adverse', 'very_adverse', 'extremely_adverse']

            if self.personnel_full_name.working_environment not in allowed_environments and self.hardship_allowance is not None:
                if self.hardship_allowance > 0:
                    raise ValidationError({
                        'hardship_allowance': (
                            'The condition should be either "adverse", "very_adverse", or "extremely_adverse" to process hardship allowance. '
                            'Please appropriately select the working environment type in the personnel list list above.'
                        )
                    })
                    # Validate university_cost_sharing_debt and cost_share_percent_to_basic_salary
            if self.personnel_full_name.university_cost_sharing_debt == Decimal(
                    0.00) or self.personnel_full_name.university_cost_sharing_debt is None:
                if self.cost_share_percent_to_basic_salary:
                    raise ValidationError({'cost_share_percent_to_basic_salary': (
                        'To pay for university cost share, you should first record the cost share debt amount on above personnel list first')})

            # validate cost share pay greater than debt Simple debt check

            # Get the debt
            debt = self.personnel_full_name.university_cost_sharing_debt or Decimal('0.00')

            # Calculate what university_cost_share_pay will be
            calculated_pay = Decimal('0.00')
            if self.personnel_full_name.basic_salary and self.cost_share_percent_to_basic_salary:
                calculated_pay = (
                        self.personnel_full_name.basic_salary *
                        (self.cost_share_percent_to_basic_salary / Decimal('100.00'))
                )

            # Sum all previous payments (excluding this one)
            total_paid = RegularPayroll.objects.filter(
                personnel_full_name=self.personnel_full_name
            ).exclude(pk=self.pk).aggregate(
                total=Sum('university_cost_share_pay')
            )['total'] or Decimal('0.00')

            # Final total if this one is added
            total_after_this = total_paid + calculated_pay

            # Validate
            if total_after_this > debt:
                raise ValidationError({
                    'cost_share_percent_to_basic_salary': (
                        f'Total cost share processed {total_after_this} exceeds the personnel\'s cost share debt {debt}. Adjust accordingly.'
                    )
                })

        super().clean()



    def save(self, *args, **kwargs):

        RegularPayrollService(self).perform_calculations()

        super().save(*args, **kwargs)


# earning adjustment
class EarningAdjustment(models.Model):
    # Choices list for different payroll components
    EARNING_ADJUSTMENT_COMPONENTS_CHOICES = [
        ('Correction and Unpaid - Fully Taxable Components', [
            ('basic_salary', 'Basic Salary'),
            ('overtime', 'Overtime'),
            ('housing_allowance', 'Housing Allowance'),
            ('position_allowance', 'Position Allowance'),
            ('commission', 'Commission'),
            ('telephone_allowance', 'Telephone Allowance'),
            ('one_time_bonus', 'One Time Bonus'),
            ('casual_labor_wage', 'Casual Labor Wage'),
        ]),

        ('Correction and Unpaid - Partially Taxable Components', [
            ('transport_home_to_office', 'Transport Home To Office'),
            ('transport_for_work', 'Transport For Work'),
            ('fuel_home_to_office', 'Fuel Home To Office'),
            ('fuel_for_work', 'Fuel For Work'),
            ('per_diem', 'Per Diem'),
            ('hardship_allowance', 'Hardship Allowance'),
        ]),

        ('Correction and Unpaid - Non-Taxable Components', [
            ('public_cash_award', 'Public Cash Award'),
            ('incidental_operation_allowance', 'Incidental Operation Allowance'),
            ('medical_allowance', 'Medical Allowance'),
            ('cash_gift', 'Cash Gift'),
            ('personal_injury', 'Personal Injury'),
            ('child_support_payment', 'Child Support Payment'),
            ('tuition_fees', 'Tuition Fees'),
        ]),

        ('DEFERRED_EARNINGS', [
            ('leave_encashment', 'Leave Encashment'),
            ('quarterly_bonus', 'Quarterly Bonus'),
            ('semi_annual_bonus', 'Semi-Annual Bonus'),
            ('annual_bonus', 'Annual Bonus'),
            ('performance_based_bonuses', 'Performance-Based Bonuses'),
            ('project_completion_bonuses', 'Project Completion Bonuses'),
            ('holiday_bonus', 'Holiday Bonus'),
            ('other_bonus', 'Other Type of Bonus'),
        ]),

    ]

    ADJUSTMENT_CASES_CHOICES = [
        ('Financial Corrections', [
            ('underpayment', 'Underpayment'),
            ('overpayment', 'Overpayment'),
            ('deduction_error', 'Deduction Error'),
            ('correction', 'Correction'),
        ]),
        ('Retroactive Changes', [
            ('salary_increment', 'Salary Increment'),
            ('backpay', 'Backpay'),
            ('contract_revision', 'Contract Revision'),
        ]),
        ('Absence or Delay', [
            ('unpaid_leave_deduction', 'Unpaid Leave Deduction'),
            ('late_payment', 'Late Payment'),
        ]),
        ('Benefit and Bonus Changes', [
            ('allowance_addition', 'Allowance Addition'),
            ('bonus_adjustment', 'Bonus Adjustment'),
        ]),
        ('Internal Movements', [
            ('transfer_adjustment', 'Transfer Adjustment'),
        ]),
        ('Other', [
            ('other', 'Other'),
        ]),
    ]

    # Model fields as described
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    #
    payroll_to_record = models.ForeignKey(RegularPayroll, on_delete=models.CASCADE, related_name='earning_adjustments')
    payroll_needing_adjustment = models.ForeignKey(RegularPayroll, on_delete=models.CASCADE)
    case = models.CharField(max_length=90, choices=ADJUSTMENT_CASES_CHOICES)

    component = models.CharField(max_length=90, choices=EARNING_ADJUSTMENT_COMPONENTS_CHOICES)
    earning_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                         validators=[MinValueValidator(Decimal('0.00'))])
    taxable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    non_taxable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    #
    employee_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                                                            blank=True)
    employer_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True,
                                                                           blank=True)
    total_pension = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # grosses
    adjusted_month_gross_taxable_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    adjusted_month_gross_non_taxable_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                                                   blank=True)
    adjusted_month_gross_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # sum of adjustment taxable and regular payroll taxable
    adjusted_month_total_taxable_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # tax
    adjusted_month_employment_income_tax_total = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                                                   blank=True)
    adjusted_month_employment_income_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                                             blank=True)

    # pension
    adjusted_month_employee_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    adjusted_month_employer_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    adjusted_month_total_pension = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    adjusted_month_total_earning_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                                                    blank=True)
    adjusted_month_expense = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # monthly
    # pension
    recorded_month_employee_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    recorded_month_employer_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    recorded_month_total_pension_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    #
    recorded_month_taxable_gross_pay = models.DecimalField(max_digits=12, decimal_places=2,
                                                                   default=Decimal('0.00'))
    recorded_month_non_taxable_gross_pay = models.DecimalField(max_digits=12, decimal_places=2,
                                                                       default=Decimal('0.00'))
    recorded_month_gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    recorded_month_total_taxable_pay = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    recorded_month_employment_income_tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    recorded_month_employment_income_tax = models.DecimalField(max_digits=12, decimal_places=2,
                                                                      default=Decimal('0.00'))
    recorded_month_total_earning_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    recorded_month_expense = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    #
    period_start = models.DateField(default=datetime.date.today)
    period_end = models.DateField(default=datetime.date.today)
    months_covered = models.IntegerField()
    created_at = models.DateField(default=datetime.date.today, blank=True,
                                  help_text="Date when this record was created")
    updated_at = models.DateField(default=datetime.date.today, help_text="Date when this record was last updated")


    def clean(self):
        # First, ensure both ForeignKeys are set
        if not self.payroll_needing_adjustment_id or not self.payroll_to_record_id:
            raise ValidationError("Both 'payroll needing adjustment' and 'record month' must be set.")

        # Safely get related objects
        payroll_adj = getattr(self, 'payroll_needing_adjustment', None)
        payroll_to_record_obj = getattr(self, 'payroll_to_record', None)

        if payroll_to_record_obj:
            personnel = getattr(payroll_to_record_obj, 'personnel_full_name', None)
            payroll_month = getattr(payroll_to_record_obj, 'payroll_month', None)

            # Example check using personnel
            if self.earning_amount and self.component == 'per_diem':
                if not personnel or not getattr(personnel, 'daily_per_diem', None) or personnel.daily_per_diem == 0:
                    raise ValidationError({
                        'earning_amount': 'To process per diem you should add daily per diem amount in personnel list.'
                    })

            allowed_environments = ['adverse', 'very_adverse', 'extremely_adverse']
            if personnel and payroll_month and self.earning_amount is not None:
                working_env = getattr(personnel, 'working_environment', None)
                if working_env not in allowed_environments and self.component == 'hardship_allowance' and self.earning_amount > 0:
                    raise ValidationError({
                        'earning_amount': (
                            'The condition should be either "adverse", "very_adverse", or "extremely_adverse" '
                            'to process hardship allowance. Please appropriately select the working environment '
                            'type in the personnel list above.'
                        )
                    })

        super().clean()



    def save(self, *args, **kwargs):
        EarningAdjustmentBusinessService(self).perform_all_calculations()
        super().save(*args, **kwargs)

    # save method
# end earning adjustment

# start deduction adjustment

class DeductionAdjustment(models.Model):
    # Choices list for different payroll components
    DEDUCTION_ADJUSTMENT_COMPONENTS_CHOICES = [

        ('Deductions and Other Adjustments', [
            ('charitable_donation', 'Charitable Donation'),
            ('saving_plan', 'Saving Plan'),
            ('loan_payment', 'Loan Payment'),
            ('court_order', 'Court Order'),
            ('workers_association', 'Workers Association'),
            ('personnel_insurance_saving', 'Personnel Insurance Saving'),
            ('red_cross', 'Red Cross'),
            ('party_contribution', 'Party Contribution'),
            ('other_deduction', 'Other Deduction'),
        ]),
    ]

    ADJUSTMENT_CASES_CHOICES = [
        ('correction', 'Correction'),
        ('overpayment', 'Overpayment'),
        ('retroactive_deduction', 'Retroactive Deduction'),
        ('deduction_adjustment', 'Deduction Adjustment'),
        ('court_order_payment', 'Court Ordered Deduction'),
        ('advance_recovery', 'Advance Recovery'),
        ('other_adjustment', 'Other Adjustment'),
    ]

    # Model fields as described
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    #
    payroll_to_record = models.ForeignKey(RegularPayroll, on_delete=models.CASCADE, related_name='deduction_adjustments')
    payroll_needing_adjustment = models.ForeignKey(RegularPayroll, on_delete=models.CASCADE)
    case = models.CharField(max_length=90, choices=ADJUSTMENT_CASES_CHOICES)

    component = models.CharField(max_length=90, choices=DEDUCTION_ADJUSTMENT_COMPONENTS_CHOICES)
    deduction_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                           validators=[MinValueValidator(Decimal('0.00'))]
                                           )

    adjusted_month_total_deduction = models.DecimalField(max_digits=12, decimal_places=2,
                                                                validators=[MinValueValidator(Decimal('0.00'))],
                                                                default=Decimal('0.00')
                                                                )

    recorded_month_total_deduction = models.DecimalField(max_digits=12, decimal_places=2,
                                                           validators=[MinValueValidator(Decimal('0.00'))],
                                                           default=Decimal('0.00')
                                                           )
    period_start = models.DateField(default=datetime.date.today)
    period_end = models.DateField(default=datetime.date.today)
    months_covered = models.IntegerField()
    created_at = models.DateField(default=datetime.date.today, blank=True,
                                  help_text="Date when this record was created")
    updated_at = models.DateField(default=datetime.date.today, help_text="Date when this record was last updated")

    def clean(self):
        if not self.payroll_needing_adjustment or not self.payroll_to_record:
            raise ValidationError("Both 'Payroll Needing Adjustment' and 'Record Month' must be set.")

    def save(self, *args, **kwargs):
        DeductionAdjustmentBusinessService(self).perform_all_calculations()  # Calculate & update fields
        super().save(*args, **kwargs)  # Save once after all updates


# end deduction adjustment

# severance pay

class SeverancePay(models.Model):
    SEVERANCE_TYPE_CHOICES = [
        ('normal', 'Normal Termination of contract'),
        ('no_notice', 'Termination Without Prior Notice'),
        ('harassment', 'Sexual Harassment'),
    ]

    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)

    severance_record_month = models.ForeignKey(PayrollPeriod, on_delete=models.PROTECT, help_text='Severance processing month')
    severance_type = models.CharField(max_length=150, choices=SEVERANCE_TYPE_CHOICES, default='normal')
    personnel_full_name = models.ForeignKey(Stakeholder, on_delete=models.SET_NULL, null=True,
                                            related_name='personnel_severance_pay')

    last_week_daily_wages = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Enter the daily wage amount for the last week. If the amount is the same throughout the month, divide the this_month_total salary by 30.'
    )
    start_date = models.DateField(help_text='Enter the start date of employment.', verbose_name='Service Start Date')
    end_date = models.DateField(help_text='Enter the end date of employment.',
                                default=datetime.date.today, verbose_name='Service End Date')

    service_years = models.PositiveIntegerField(blank=True)
    service_days = models.PositiveIntegerField(blank=True)

    severance_for_years = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    severance_for_days = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    gross_severance_pay = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    prorate_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    employment_income_tax_from_basic_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    total_employment_income_tax_from_basic_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    employment_income_tax_from_prorate_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    employment_income_tax_from_severance_pay = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    net_severance_pay = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    def __str__(self):
        return str(self.personnel_full_name)

    class Meta:
        verbose_name = "             Severance Pay"
        verbose_name_plural = "             Severance Pay"
        ordering = ['-id']  # You can change the ordering field as needed

    def clean(self):
        if self.start_date and self.end_date:
            self.service_years = (self.end_date - self.start_date).days
            # Validate service years
            if self.service_years and self.service_years < 365:
                raise ValidationError({'start_date': 'No clear directive for severance pay for less than a year.'})
        super().clean()

    def save(self, *args, **kwargs):
        """
        Overridden save method to delegate all business logic to service class.
        Keeps model logic clean.
        """
        SeverancePayService(self).compute()
        super().save(*args, **kwargs)



class Vision(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    vision_statement = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.vision_statement} - {self.organization_name}"

    @property
    def display_vision_statement(self):
        from management_project.services.vision import VisionService
        return VisionService.get_display_statement(self.organization_name.organization_name, self.vision_statement)


class Mission(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    mission_statement = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.mission_statement} - {self.organization_name}"

    @property
    def display_mission_statement(self):
        from management_project.services.mission import MissionService
        return MissionService.get_display_statement(self.organization_name.organization_name, self.mission_statement)