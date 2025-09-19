from django import forms
from .models import *
from management_project.services.vision import VisionService
from management_project.services.mission import MissionService
from management_project.services.swot import SwotChoicesService
from .services.swot import SwotChoicesService
from .services.strategy_map import StrategyMapChoicesService

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
            'organization_name',
        ]

        widgets = {
            'stakeholder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stakeholder Name'}),
            'stakeholder_type': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department or Team'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description'}),
            'impact_level': forms.Select(attrs={'class': 'form-control'}),
            'interest_level': forms.Select(attrs={'class': 'form-control'}),
            'engagement_strategy': forms.Select(attrs={'class': 'form-control'}),
            'influence_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Influence Score'}),
            'priority': forms.Select(
                attrs={ 'class': 'form-select',  'id': 'priority',}
            ),
            'satisfaction_level': forms.Select(attrs={'class': 'form-control'}),
            'risk_level': forms.Select(attrs={'class': 'form-control'}),
            'contribution_score': forms.Select(
                attrs={ 'class': 'form-select', 'id': 'contribution_score',}
            ),
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


class StrategicCycleForm(forms.ModelForm):
    class Meta:
        model = StrategicCycle
        fields = [
            'time_horizon',
            'time_horizon_type',
            'start_date',
            'end_date',
        ]
        widgets = {
            'time_horizon': forms.Select(attrs={'class': 'form-select'}),
            'time_horizon_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: style help text
        for field_name, field in self.fields.items():
            if field.help_text:
                field.help_text = f'<span style="color: blue; font-style: italic;">{field.help_text}</span>'


class StrategicActionPlanForm(forms.ModelForm):

    class Meta:
        model = StrategicActionPlan
        exclude = ['organization_name', 'improvement_needed',]
        widgets = {
            # Foreign keys
            'strategic_cycle': forms.Select(attrs={'class': 'form-control'}),
            'strategy_map': forms.Select(attrs={'class': 'form-control'}),
            'responsible_bodies': forms.SelectMultiple(attrs={'class': 'form-control'}),

            # KPI & Measurement
            'indicator_type': forms.Select(attrs={'class': 'form-control'}),
            'direction_of_change': forms.Select(attrs={'class': 'form-control'}),
            'baseline': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter baseline value'}),
            'target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter target value'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Weight'}),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Organization-specific filtering
        if self.request and self.request.user.is_authenticated and hasattr(self.request.user, 'organization_name'):
            org = self.request.user.organization_name
            self.fields['strategic_cycle'].queryset = StrategicCycle.objects.filter(organization_name=org)
            self.fields['strategy_map'].queryset = StrategyMap.objects.filter(organization_name=org)
            self.fields['responsible_bodies'].queryset = Stakeholder.objects.filter(organization_name=org)
        else:
            self.fields['strategic_cycle'].queryset = StrategicCycle.objects.none()
            self.fields['strategy_map'].queryset = StrategyMap.objects.none()
            self.fields['responsible_bodies'].queryset = Stakeholder.objects.none()

        # Add invalid bootstrap styling for error fields
        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', 'form-control')
            if field_name in self.errors:
                css_classes += ' is-invalid'
            field.widget.attrs['class'] = css_classes

    error_css_class = 'text-danger'
    required_css_class = 'font-weight-bold'


#strategy report

class StrategicReportForm(forms.ModelForm):
    action_plan = forms.ModelChoiceField(
        queryset=StrategicActionPlan.objects.none(),  # initially empty
        label="Action Plan",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': '',  # optional, will set via __init__
        }),
        empty_label="Select Action Plan"
    )

    class Meta:
        model = StrategicReport
        fields = [
            'action_plan', 'achievement', 'data_source',
            'data_collector', 'progress_summary', 'performance_summary', 'status'
        ]
        widgets = {
            'achievement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data_source': forms.TextInput(attrs={'class': 'form-control'}),
            'data_collector': forms.TextInput(attrs={'class': 'form-control'}),
            'progress_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'performance_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Filter by user organization
        if self.request and self.request.user.is_authenticated and hasattr(self.request.user, 'organization_name'):
            org = self.request.user.organization_name
            qs = StrategicActionPlan.objects.filter(organization_name=org)
        else:
            qs = StrategicActionPlan.objects.none()

        # # If editing, ensure current instance is included
        # if getattr(self.instance, 'action_plan', None):
        #     qs = qs | StrategicActionPlan.objects.filter(pk=self.instance.action_plan.pk)
        #
        # self.fields['action_plan'].queryset = qs
        #
        # # Set tooltip for each option
        # for plan in qs:
        #     self.fields['action_plan'].widget.attrs['title'] = plan.get_full_label()

        # If we're editing and the instance has an action_plan, ensure it's included
        instance_plan = getattr(self.instance, 'action_plan', None)
        if instance_plan:
            qs = (qs | StrategicActionPlan.objects.filter(pk=instance_plan.pk)).distinct()

        self.fields['action_plan'].queryset = qs




# class StrategicReportForm(forms.ModelForm):
#     class Meta:
#         model = StrategicReport
#         fields = [
#             'action_plan',
#             'achievement',
#             'data_source',
#             'data_collector',
#             'progress_summary',
#             'performance_summary',
#         ]
#         widgets = {
#             'action_plan': forms.Select(attrs={
#                 'class': 'form-control',
#                 'style': 'height: auto; min-height: 100px;'  # Make dropdown taller
#             }),
#             # 'action_plan': forms.Select(attrs={'class': 'form-control'}),
#             'achievement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'data_source': forms.TextInput(attrs={'class': 'form-control'}),
#             'data_collector': forms.TextInput(attrs={'class': 'form-control'}),
#             'progress_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'performance_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#
#         # Filter action plans by user organization
#         if self.request and self.request.user.is_authenticated and hasattr(self.request.user, 'organization_name'):
#             org = self.request.user.organization_name
#             self.fields['action_plan'].queryset = StrategicActionPlan.objects.filter(organization_name=org)
#         else:
#             self.fields['action_plan'].queryset = StrategicActionPlan.objects.none()


#deduction adjustment

class DeductionAdjustmentForm(forms.ModelForm):
    payroll_to_record = forms.ModelChoiceField(
        queryset=StrategicActionPlan.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    payroll_needing_adjustment = forms.ModelChoiceField(
        queryset=StrategicActionPlan.objects.all(),
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
            self.fields['payroll_needing_adjustment'].queryset = StrategicActionPlan.objects.filter(
                organization_name=org
            )
            self.fields['payroll_to_record'].queryset = StrategicActionPlan.objects.filter(
                organization_name=org
            )
        else:
            self.fields['payroll_needing_adjustment'].queryset = StrategicActionPlan.objects.none()
            self.fields['payroll_to_record'].queryset = StrategicActionPlan.objects.none()


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



class ValuesForm(forms.ModelForm):
    class Meta:
        model = Values
        fields = ['values']
        widgets = {
            'values': forms.Select(
                attrs={'class': 'form-control'},
                choices=ValuesService.VALUE_CHOICES
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure choices always follow grouped <optgroup> style
        self.fields['values'].choices = ValuesService.VALUE_CHOICES



class SwotAnalysisForm(forms.ModelForm):
    class Meta:
        model = SwotAnalysis
        fields = [
            'swot_type', 'swot_pillar', 'swot_factor',
            'priority', 'impact', 'likelihood', 'description'
        ]
        widgets = {
            'swot_type': forms.Select(attrs={'class': 'form-control'}),
            'swot_pillar': forms.Select(attrs={'class': 'form-control'}),
            'swot_factor': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'impact': forms.Select(attrs={'class': 'form-control'}),
            'likelihood': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        swot_type = self.data.get('swot_type') or getattr(self.instance, 'swot_type', None)
        pillar = self.data.get('swot_pillar') or getattr(self.instance, 'swot_pillar', None)

        # Level 1: SWOT Type
        self.fields['swot_type'].choices = [('', '--- Select SWOT Type ---')] + SwotChoicesService.get_swot_type_choices()

        # Level 2: Pillar
        if swot_type:
            self.fields['swot_pillar'].choices = [('', '--- Select Pillar ---')] + SwotChoicesService.get_pillar_choices(swot_type)
            self.fields['swot_pillar'].widget.attrs.pop('disabled', None)
        else:
            self.fields['swot_pillar'].choices = [('', '--- Select Type First ---')]
            self.fields['swot_pillar'].widget.attrs['disabled'] = True

        # Level 3: Factor
        if swot_type and pillar:
            self.fields['swot_factor'].choices = [('', '--- Select Factor ---')] + SwotChoicesService.get_factor_choices(swot_type, pillar)
            self.fields['swot_factor'].widget.attrs.pop('disabled', None)
        else:
            self.fields['swot_factor'].choices = [('', '--- Select Pillar First ---')]
            self.fields['swot_factor'].widget.attrs['disabled'] = True


class StrategyMapForm(forms.ModelForm):
    # Include formula in the form explicitly
    formula = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'readonly': 'readonly',
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Select KPI to see formula'
        }),
        label="KPI Formula"
    )

    class Meta:
        model = StrategyMap
        # Include formula in fields so it is rendered
        fields = ['strategic_perspective', 'strategic_pillar', 'objective', 'kpi', 'formula',]
        widgets = {
            'strategic_perspective': forms.Select(attrs={'class': 'form-control'}),
            'strategic_pillar': forms.Select(attrs={'class': 'form-control'}),
            'objective': forms.Select(attrs={'class': 'form-control'}),
            'kpi': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load current selections
        perspective = self.data.get('strategic_perspective') or getattr(self.instance, 'strategic_perspective', None)
        pillar = self.data.get('strategic_pillar') or getattr(self.instance, 'strategic_pillar', None)
        objective = self.data.get('objective') or getattr(self.instance, 'objective', None)
        kpi = self.data.get('kpi') or getattr(self.instance, 'kpi', None)

        # Populate dropdowns dynamically
        self.fields['strategic_perspective'].choices = [('', '--- Select Perspective ---')] + StrategyMapChoicesService.get_perspective_choices()

        if perspective:
            self.fields['strategic_pillar'].choices = [('', '--- Select Pillar ---')] + StrategyMapChoicesService.get_pillar_choices(perspective)
        else:
            self.fields['strategic_pillar'].choices = [('', '--- Select Perspective First ---')]
            self.fields['strategic_pillar'].widget.attrs['disabled'] = True

        if perspective and pillar:
            self.fields['objective'].choices = [('', '--- Select Objective ---')] + StrategyMapChoicesService.get_objective_choices(perspective, pillar)
        else:
            self.fields['objective'].choices = [('', '--- Select Pillar First ---')]
            self.fields['objective'].widget.attrs['disabled'] = True

        if perspective and pillar and objective:
            self.fields['kpi'].choices = [('', '--- Select KPI ---')] + StrategyMapChoicesService.get_kpi_choices(perspective, pillar, objective)
        else:
            self.fields['kpi'].choices = [('', '--- Select Objective First ---')]
            self.fields['kpi'].widget.attrs['disabled'] = True

        # Auto-fill formula
        if perspective and pillar and objective and kpi:
            self.fields['formula'].initial = StrategyMapChoicesService.get_formula(perspective, pillar, objective, kpi)
        else:
            self.fields['formula'].initial = "Select a KPI to see the formula"