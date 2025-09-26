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

from .services.values import ValuesService
import calendar



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




class SwotAnalysis(models.Model):
    SWOT_TYPES = [
        ('Strength', 'Strength'),
        ('Weakness', 'Weakness'),
        ('Opportunity', 'Opportunity'),
        ('Threat', 'Threat'),
    ]

    PRIORITY_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
    ]

    IMPACT_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
    ]

    LIKELIHOOD_CHOICES = [
        ('Almost Certain', 'Almost Certain'),
        ('Likely', 'Likely'),
        ('Possible', 'Possible'),
        ('Unlikely', 'Unlikely'),
        ('Rare', 'Rare'),
    ]

    organization_name = models.ForeignKey(
        OrganizationalProfile, on_delete=models.PROTECT
    )
    swot_type = models.CharField(max_length=20, choices=SWOT_TYPES)
    swot_pillar = models.CharField(max_length=100)
    swot_factor = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, default="Medium")
    likelihood = models.CharField(max_length=20, choices=LIKELIHOOD_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["swot_type", "priority", "-created_at"]

    def __str__(self):
        return f"{self.swot_type} → {self.swot_pillar} → {self.swot_factor[:50]}"



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




class Values(models.Model):
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)

    values = models.CharField(
        max_length=50,
        choices=[(key, label) for group in ValuesService.VALUE_CHOICES for key, label in group[1]],
        unique=True
    )

    def get_category(self):
        for group_name, group_values in ValuesService.VALUE_CHOICES:
            for key, label in group_values:
                if key == self.values:
                    return group_name
        return None

    def __str__(self):
        return self.get_values_display()


class StrategyHierarchy(models.Model):
    organization_name = models.ForeignKey(
        OrganizationalProfile, on_delete=models.PROTECT
    )
    strategic_perspective = models.CharField(max_length=100)
    focus_area = models.CharField(max_length=100)
    objective = models.CharField(max_length=100)
    kpi = models.CharField(max_length=100, verbose_name='Key Performance Indicator')
    formula = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.strategic_perspective} → {self.focus_area} → {self.objective} → {self.kpi}"



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
        ('funder', 'Funder'),
        ('regulator', 'Regulator'),
        ('community', 'Community'),
        ('consultant', 'Consultant'),
        ('advisor', 'Advisor'),
        ('board_member', 'Board Member'),
        ('volunteer', 'Volunteer'),
        ('contractor', 'Contractor'),
        ('researcher', 'Researcher'),
        ('media', 'Media'),
        ('government_official', 'Government Official'),
        ('auditor', 'Auditor'),
        ('legal', 'Legal Counsel'),
        ('finance', 'Finance'),
        ('hr', 'Human Resources'),
        ('it', 'IT Support'),
        ('operations', 'Operations'),
        ('logistics', 'Logistics'),
        ('product_owner', 'Product Owner'),
        ('scrum_master', 'Scrum Master'),
        ('analyst', 'Business Analyst'),
        ('trainer', 'Trainer'),
        ('mentor', 'Mentor'),
        ('intern', 'Intern'),
        ('other', 'Other'),
    ]

    IMPACT_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    INTEREST_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]

    ENGAGEMENT_STRATEGY_CHOICES = [
        ('inform', 'Inform'),
        ('consult', 'Consult'),
        ('involve', 'Involve'),
        ('collaborate', 'Collaborate'),
        ('empower', 'Empower'),
    ]

    SATISFACTION_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]

    RISK_LEVEL_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    PRIORITY_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    CONTRIBUTION_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]

    # ------------------ Core Info ------------------
    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    stakeholder_name = models.CharField(max_length=200, help_text='Stakeholder name or organization')
    stakeholder_type = models.CharField(max_length=20, choices=STAKEHOLDER_TYPE_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True, help_text='Optional department or team')

    # ------------------ Analysis ------------------
    impact_level = models.CharField(max_length=20, choices=IMPACT_LEVEL_CHOICES, default='medium')
    interest_level = models.CharField(max_length=20, choices=INTEREST_LEVEL_CHOICES, default='medium')
    engagement_strategy = models.CharField(max_length=20, choices=ENGAGEMENT_STRATEGY_CHOICES, default='inform')
    influence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                          help_text='Quantitative measure of influence')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium',
                                help_text='Calculated from impact x interest x influence')
    satisfaction_level = models.CharField(max_length=20, choices=SATISFACTION_LEVEL_CHOICES, default='medium',
                                          help_text='Stakeholder satisfaction with the project or SaaS')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='medium',
                                  help_text='Potential risk if stakeholder is disengaged')
    contribution_score = models.CharField(max_length=10, choices=CONTRIBUTION_CHOICES, default='medium',
                                          help_text='Estimated contribution to strategic objectives')

    # ------------------ Contact ------------------
    contact_info = models.CharField(max_length=200, blank=True, null=True,
                                    help_text='Email, phone, or other contact details')
    notes = models.TextField(blank=True, null=True, help_text='Additional observations or comments')
    description = models.TextField(blank=True, null=True, help_text='Brief description of the stakeholder')

    class Meta:
        ordering = ["-priority", "stakeholder_name"]

    def __str__(self):
        return f"{self.stakeholder_name} ({self.get_role_display()})"

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


class StrategicCycle(models.Model):
    TIME_HORIZON_CHOICES = [
        ('10 years', '10 years'),
        ('5 years', '5 years'),
        ('3 years', '3 years'),
        ('2 years', '2 years'),
        ('1 year', '1 year'),
        ('6 months', '6 months'),
        ('Quarterly', 'Quarterly'),
        ('Monthly', 'Monthly'),
    ]

    TIME_HORIZON_TYPE_CHOICES = [
        ('Long Term', 'Long Term'),
        ('Medium Term', 'Medium Term'),
        ('Short Term', 'Short Term'),
    ]

    organization_name = models.ForeignKey(
        'OrganizationalProfile',
        on_delete=models.PROTECT,
        related_name='strategic_cycles'
    )
    name = models.CharField(max_length=100, help_text='Descriptive name for the strategic cycle')
    time_horizon = models.CharField(max_length=20, choices=TIME_HORIZON_CHOICES)
    time_horizon_type = models.CharField(max_length=20, choices=TIME_HORIZON_TYPE_CHOICES)
    start_date = models.DateField(help_text='Exact start date of the strategic cycle')
    end_date = models.DateField(help_text='Exact end date of the strategic cycle / report date')

    # New fields to store calculated values

    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = "Strategic Cycle"
        verbose_name_plural = "Strategic Cycles"
        ordering = ['start_date', '-id']

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    @property
    def start_month_name(self):
        return calendar.month_name[self.start_date.month]

    @property
    def start_quarter(self):
        return (self.start_date.month - 1) // 3 + 1

    @property
    def start_year(self):
        return self.start_date.year

    def save(self, *args, **kwargs):
        # Auto-generate name based on org + time horizon + dates
        self.name = f"{self.organization_name} - {self.time_horizon} ({self.start_date:%B %Y}–{self.end_date:%B %Y})"

        if not self.slug:
            # Build slug from multiple fields
            base_slug = slugify(
                f"{self.name}-"
                f"{self.time_horizon}-{self.time_horizon_type}-"
                f"{self.start_date}-{self.end_date}"
            )
            slug = base_slug
            counter = 1
            while StrategicCycle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)



    def __str__(self):
        start_str = self.start_date.strftime("%Y-%m-%d") if self.start_date else "N/A"
        end_str = self.end_date.strftime("%Y-%m-%d") if self.end_date else "N/A"
        return f"{self.organization_name} - {self.name} ({self.time_horizon_type}, {start_str} → {end_str})"


class StrategicActionPlan(models.Model):
    # stakeholder_list information
    INDICATOR_TYPE_CHOICES = [
        ('Lead', 'Lead'),
        ('Lagg', 'Lagg'),
    ]

    DIRECTION_OF_CHANGE_CHOICES = [
        ('Increasing', 'Increasing'),
        ('Decreasing', 'Decreasing'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    organization_name = models.ForeignKey(
        OrganizationalProfile, on_delete=models.PROTECT, verbose_name='Owner / Responsible Party'
    )
    # Parent references
    strategic_cycle = models.ForeignKey(
        'StrategicCycle',
        on_delete=models.CASCADE,
        related_name='action_plans'
    )
    strategy_hierarchy = models.ForeignKey(
        'StrategyHierarchy',
        on_delete=models.CASCADE,
        related_name='action_plans'
    )
    responsible_bodies = models.ManyToManyField(
        'Stakeholder', blank=True, related_name='action_plans'
    )

    # KPI & Measurement
    indicator_type = models.CharField(max_length=10, choices=INDICATOR_TYPE_CHOICES)
    direction_of_change = models.CharField(max_length=10, choices=DIRECTION_OF_CHANGE_CHOICES)
    baseline = models.DecimalField(max_digits=22, decimal_places=2)
    target = models.DecimalField(max_digits=22, decimal_places=2)
    improvement_needed = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES,
        default='pending', help_text="Current status of the strategic plan"
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=100,
        help_text="Weight of this Action Plan KPI relative to other KPI per strategic cycle"
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2)



    class Meta:
        verbose_name = "Strategic Action Plan"
        verbose_name_plural = "Strategic Action Plans"
        ordering = ['strategic_cycle__start_date', '-id']



    def save(self, *args, **kwargs):

        # Calculate improvement_needed and duration
        if self.baseline is not None and self.target is not None:
            self.improvement_needed = self.target - self.baseline

        super().save(*args, **kwargs)

    def responsible_bodies_display(self):
        return ", ".join([str(s) for s in self.responsible_bodies.all()])

    def get_full_display(self):
        """Full info for tooltip"""
        cycle_name = (
            f"{self.strategic_cycle.name} - {self.strategic_cycle.time_horizon} - "
            f"{self.strategic_cycle.time_horizon_type} - {self.strategic_cycle.start_date} - "
            f"{self.strategic_cycle.end_date}" if self.strategic_cycle else "N/A"
        )
        kpi = self.strategy_hierarchy.kpi if self.strategy_hierarchy else "N/A"
        baseline = self.baseline or 0
        target = self.target or 0
        responsible = self.responsible_bodies_display() or "N/A"

        return f"{cycle_name} | KPI: {kpi} | Baseline: {baseline} | Target: {target} | Responsible: {responsible}"

    def __str__(self):
        """Single-line label for dropdown"""
        if self.strategic_cycle:
            start = self.strategic_cycle.start_date.strftime("%B %d, %Y") if self.strategic_cycle.start_date else "N/A"
            end = self.strategic_cycle.end_date.strftime("%B %d, %Y") if self.strategic_cycle.end_date else "N/A"
            cycle_name = f"{self.strategic_cycle.name} - {self.strategic_cycle.time_horizon} - {self.strategic_cycle.time_horizon_type} - {start} - {end}"
        else:
            cycle_name = "N/A"

        kpi = self.strategy_hierarchy.kpi if self.strategy_hierarchy else "N/A"
        baseline = self.baseline or 0
        target = self.target or 0
        responsible = self.responsible_bodies_display() or "N/A"

        return f"{cycle_name} | KPI: {kpi} | Baseline: {baseline} | Target: {target} | Responsible: {responsible}"


    def dropdown_label_lines(self):
        """Return tuple/list of lines for display in the radio label."""
        if self.strategic_cycle:
            start = self.strategic_cycle.start_date.strftime("%B %d, %Y") if self.strategic_cycle.start_date else "N/A"
            end = self.strategic_cycle.end_date.strftime("%B %d, %Y") if self.strategic_cycle.end_date else "N/A"
            cycle_line = f"{self.strategic_cycle.name} ({start} - {end})"
        else:
            cycle_line = "Cycle: N/A"

        kpi = self.strategy_hierarchy.kpi if self.strategy_hierarchy else "N/A"
        baseline = self.baseline or 0
        target = self.target or 0
        resp = self.responsible_bodies_display() or "N/A"

        return [
            cycle_line,
            f"KPI: {kpi}",
            f"Baseline: {baseline} | Target: {target}",
            f"Responsible: {resp}",
        ]


# strategic report
class StrategicReport(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    organization_name = models.ForeignKey(OrganizationalProfile, on_delete=models.PROTECT)
    action_plan = models.ForeignKey(
        StrategicActionPlan, on_delete=models.CASCADE, related_name="reports"
    )
    achievement = models.DecimalField(max_digits=22, decimal_places=2, default=0)
    percent_achieved = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    variance = models.DecimalField(max_digits=22, decimal_places=2, default=0)
    weighted_score = models.DecimalField(max_digits=22, decimal_places=2, default=0)
    data_source = models.CharField(max_length=200, blank=True, null=True)
    data_collector = models.CharField(max_length=200, blank=True, null=True)
    progress_summary = models.TextField(blank=True, null=True)
    performance_summary = models.TextField(blank=True, null=True)
    # Optional qualitative fields
    challenges = models.TextField(blank=True, null=True)
    successes = models.TextField(blank=True, null=True)
    lessons_learned = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='pending', help_text="Current status of the strategic plan"
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = "Strategic Report"
        verbose_name_plural = "Strategic Reports"

    def save(self, *args, **kwargs):

        plan = self.action_plan
        # Ensure percent achieved and variance
        baseline = plan.baseline or 0
        target = plan.target or 0
        actual = self.achievement
        self.percent_achieved = ((actual - baseline) / (target - baseline) * 100) if target != baseline else 0
        self.variance = target - actual
        self.weighted_score = actual * (plan.weight / 100)
        self.responsible_body = plan.responsible_bodies_display()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.action_plan.strategic_cycle.time_horizon} | "
            f"Start: {self.action_plan.strategic_cycle.start_date:%B %d, %Y} | "
            f"End: {self.action_plan.strategic_cycle.end_date:%B %d, %Y}"
        )


class SwotReport(models.Model):
    SWOT_TYPES = [
        ('Strength', 'Strength'),
        ('Weakness', 'Weakness'),
        ('Opportunity', 'Opportunity'),
        ('Threat', 'Threat'),
    ]

    PRIORITY_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
    ]

    IMPACT_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
    ]

    LIKELIHOOD_CHOICES = [
        ('Almost Certain', 'Almost Certain'),
        ('Likely', 'Likely'),
        ('Possible', 'Possible'),
        ('Unlikely', 'Unlikely'),
        ('Rare', 'Rare'),
    ]

    organization_name = models.ForeignKey(
        OrganizationalProfile, on_delete=models.PROTECT
    )
    strategic_report_period = models.ForeignKey(
        StrategicReport, on_delete=models.CASCADE
    )
    swot_type = models.CharField(max_length=20, choices=SWOT_TYPES)
    swot_pillar = models.CharField(max_length=100)
    swot_factor = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, default="Medium")
    likelihood = models.CharField(max_length=20, choices=LIKELIHOOD_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["swot_type", "priority", "-created_at"]

    def __str__(self):
        return f"{self.swot_type} → {self.swot_pillar} → {self.swot_factor[:50]}"