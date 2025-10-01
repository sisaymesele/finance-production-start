from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from management_project.models import (
    OrganizationalProfile, SwotAnalysis, Vision, Mission, Values, StrategyHierarchy,
    Stakeholder, StrategicCycle, StrategicActionPlan, StrategicReport, SwotReport, Initiative,
    InitiativeTimeline, InitiativeBudget, InitiativeResource
)
from management_project.forms import (
    OrganizationalProfileForm, SwotAnalysisForm, VisionForm, MissionForm, ValuesForm,
    StrategyHierarchyForm, StakeholderForm, StrategicCycleForm, StrategicActionPlanForm,
    StrategicReportForm, SwotReportForm, InitiativeForm, InitiativeTimelineForm,
    InitiativeBudgetForm, InitiativeResourceForm
)

# Register your models here.
@admin.register(OrganizationalProfile)
class OrganizationalProfileAdmin(admin.ModelAdmin):
    form = OrganizationalProfileForm
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

@admin.register(SwotAnalysis)
class SwotAnalysisAdmin(admin.ModelAdmin):
    form = SwotAnalysisForm
    list_display = (
        'organization_name', 'swot_type', 'swot_pillar', 'swot_factor', 'priority',
        'impact', 'likelihood', 'created_at',
    )
    list_filter = ('swot_type', 'priority', 'impact', 'likelihood', 'organization_name')
    search_fields = ('swot_pillar', 'swot_factor', 'description')

    # Restrict foreign key choices based on logged-in user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                kwargs['queryset'] = OrganizationalProfile.objects.filter(
                    pk=request.user.organization_name.pk
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset so non-superusers only see their org's data
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


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    form = MissionForm

    # Display these fields in the list view
    list_display = ('organization_name', 'mission_statement')

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


@admin.register(Values)
class ValuesAdmin(admin.ModelAdmin):
    form = ValuesForm

    # Display these fields in the list view
    list_display = ('organization_name', 'values', 'get_category')

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




@admin.register(StrategyHierarchy)
class StrategyHierarchyAdmin(admin.ModelAdmin):
    form = StrategyHierarchyForm

    list_display = (
        'organization_name', 'strategic_perspective', 'focus_area', 'objective', 'kpi', 'formula',
    )
    list_filter = ('strategic_perspective', 'focus_area', 'organization_name')
    search_fields = ('objective', 'kpi', 'formula')

    # Restrict foreign key choices based on logged-in user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                kwargs['queryset'] = OrganizationalProfile.objects.filter(
                    pk=request.user.organization_name.pk
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset so non-superusers only see their org's data
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()



@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    form = StakeholderForm

    # Fields to display in the list view
    list_display = (
        'organization_name', 'stakeholder_name', 'role', 'stakeholder_type',
        'impact_level', 'interest_level', 'engagement_strategy',
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


@admin.register(StrategicCycle)
class StrategicCycleAdmin(admin.ModelAdmin):
    form = StrategicCycleForm

    # Display model fields
    list_display = [
        'organization_name', 'time_horizon', 'time_horizon_type',
        'start_date', 'end_date', 'duration_days', 'slug'
    ]

    # Filters
    list_filter = ['organization_name', 'time_horizon_type', 'time_horizon']
    search_fields = ['time_horizon', 'slug']
    ordering = ['-start_date']

    readonly_fields = ['slug']

    # Restrict foreign keys based on user's organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs['queryset'] = OrganizationalProfile.objects.filter(pk=org.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset to user's organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()

# #
@admin.register(StrategicActionPlan)
class StrategicActionPlanAdmin(admin.ModelAdmin):
    form = StrategicActionPlanForm
    list_display = ['organization_name', 'get_perspective', 'get_pillar', 'get_objective', 'get_kpi', 'get_formula',
                    'indicator_type', 'direction_of_change', 'baseline', 'target', 'improvement_needed', 'get_time_horizon',
                    'get_time_horizon_type', 'get_start_date', 'get_end_date', 'get_duration_days',
                    'get_responsible_bodies', 'status', 'weight', 'budget']

    # Custom display methods
    def get_perspective(self, obj):
        return obj.strategy_hierarchy.strategic_perspective

    get_perspective.short_description = "Perspective"

    def get_pillar(self, obj):
        return obj.strategy_hierarchy.focus_area

    get_pillar.short_description = "Pillar"

    def get_objective(self, obj):
        return obj.strategy_hierarchy.objective

    get_objective.short_description = "Objective"

    def get_kpi(self, obj):
        return obj.strategy_hierarchy.kpi

    get_kpi.short_description = "KPI"

    def get_formula(self, obj):
        return obj.strategy_hierarchy.formula

    get_formula.short_description = "Formula"

    def get_time_horizon(self, obj):
        return obj.strategic_cycle.time_horizon

    get_time_horizon.short_description = "Time Horizon"

    def get_time_horizon_type(self, obj):
        return obj.strategic_cycle.time_horizon_type

    get_time_horizon_type.short_description = "Horizon Type"

    def get_start_date(self, obj):
        return obj.strategic_cycle.start_date

    get_start_date.short_description = "Start Date"

    def get_end_date(self, obj):
        return obj.strategic_cycle.end_date

    get_end_date.short_description = "End Date"

    def get_duration_days(self, obj):
        return obj.strategic_cycle.duration_days

    get_duration_days.short_description = "Duration (Days)"

    def get_responsible_bodies(self, obj):
        return ", ".join([body.stakeholder_name for body in obj.responsible_bodies.all()])

    get_responsible_bodies.short_description = "Responsible Bodies"

    list_filter = ['organization_name', 'strategic_cycle', 'strategy_hierarchy', 'indicator_type', 'direction_of_change']

    search_fields = [
        'key_performance_indicator',
        'strategy_hierarchy__objective',
        'strategy_hierarchy__kpi'
    ]

    filter_horizontal = ('responsible_bodies',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(organization_name=org)
            if db_field.name == 'strategic_cycle':
                kwargs["queryset"] = StrategicCycle.objects.filter(organization_name=org)
            if db_field.name == 'strategy_hierarchy':
                kwargs["queryset"] = StrategyHierarchy.objects.filter(organization_name=org)
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


@admin.register(StrategicReport)
class StrategicReportAdmin(admin.ModelAdmin):
    form = StrategicReportForm
    list_display = (
        'organization_name', 'action_plan', 'achievement', 'percent_achieved', 'variance', 'weighted_score',
        'data_source', 'data_collector', 'progress_summary', 'performance_summary',
        'challenges', 'successes', 'lessons_learned', 'status', 'created_at', 'updated_at',
    )

    list_filter = ('action_plan', 'organization_name',)
    search_fields = ('action_plan__strategy_hierarchy__key_performance_indicator', 'responsible_body', 'organization_name__organization_name')
    ordering = ('-created_at',)

    readonly_fields = ( 'percent_achieved', 'variance', 'weighted_score', 'created_at', 'updated_at',)

    # Filter foreign keys based on user organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'organization_name':
                kwargs["queryset"] = OrganizationalProfile.objects.filter(id=org.id)
            if db_field.name == 'action_plan':
                kwargs["queryset"] = StrategicActionPlan.objects.filter(organization_name=org)
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


# -------------------------------
# SwotReport Admin
# -------------------------------
@admin.register(SwotReport)
class SwotReportAdmin(admin.ModelAdmin):
    form = SwotReportForm

    list_display = (
        'organization_name', 'strategic_report_period', 'swot_type', 'swot_pillar', 'swot_factor',
        'priority', 'impact', 'likelihood', 'description', 'created_at', 'updated_at'
    )

    list_filter = ('swot_type', 'swot_pillar', 'priority', 'impact')
    search_fields = (
        'strategic_report_period__action_plan__strategy_hierarchy__key_performance_indicator',
        'swot_factor', 'description'
    )
    ordering = ('-strategic_report_period__created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Pass request to the form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['request'] = request  # Pass request to the form for filtering
        return form_kwargs

    # Filter foreign key dropdowns by user's organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name

            if db_field.name == 'strategic_report_period':
                kwargs['queryset'] = StrategicReport.objects.filter(organization_name=org)

            elif db_field.name == 'organization_name':
                kwargs['queryset'] = OrganizationalProfile.objects.filter(pk=org.pk)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Filter admin list view by user's organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    form = InitiativeForm
    list_display = ('initiative_focus_area', 'initiative_dimension', 'initiative_name', 'priority',
                    'impact', 'likelihood', 'risk_level', 'status', 'organization_name', 'created_at')
    list_filter = ('initiative_focus_area', 'initiative_dimension', 'priority', 'status', 'organization_name')
    search_fields = ('initiative_name', 'description')
    ordering = ('-created_at',)

    # Restrict organization for non-superusers
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                kwargs['queryset'] = OrganizationalProfile.objects.filter(
                    pk=request.user.organization_name.pk
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Filter queryset for non-superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()


@admin.register(InitiativeTimeline)
class InitiativeTimelineAdmin(admin.ModelAdmin):
    form = InitiativeTimelineForm

    # Fields to display in the admin list view
    list_display = ['organization_name', 'initiative', 'start_date', 'end_date', 'remaining_days', 'remaining_months']
    list_filter = ['organization_name', 'initiative']
    search_fields = ['initiative__initiative_name']
    ordering = ['-start_date']

    readonly_fields = ['remaining_days', 'remaining_months']

    # Filter foreign keys by logged-in user's organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'initiative' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs['queryset'] = Initiative.objects.filter(organization_name=org)
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs['queryset'] = OrganizationalProfile.objects.filter(pk=org.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset to user's organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()

    # Pass request to form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['request'] = request
        return form_kwargs


@admin.register(InitiativeBudget)
class InitiativeBudgetAdmin(admin.ModelAdmin):
    form = InitiativeBudgetForm

    # Fields to display in admin list view
    list_display = [
        'organization_name', 'initiative', 'budget_type', 'budget_name',
        'budget_source', 'currency', 'budget_plan', 'budget_used', 'created_at', 'updated_at'
    ]

    list_filter = ['organization_name', 'initiative', 'budget_type', 'currency']
    search_fields = ['budget_name', 'budget_source', 'initiative__initiative_name']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at']

    # Filter foreign keys by logged-in user's organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'initiative' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs['queryset'] = Initiative.objects.filter(organization_name=org)
        if db_field.name == 'organization_name' and not request.user.is_superuser:
            if hasattr(request.user, 'organization_name'):
                org = request.user.organization_name
                kwargs['queryset'] = OrganizationalProfile.objects.filter(pk=org.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset to user's organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()

    # Pass request to form for filtering initiative dropdown
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['request'] = request
        return form_kwargs


@admin.register(InitiativeResource)
class InitiativeResourceAdmin(admin.ModelAdmin):
    form = InitiativeResourceForm

    # Fields to display in the admin list view
    list_display = [
        'organization_name', 'initiative', 'resource_type', 'resource_name',
        'resource_required', 'resource_used', 'resource_remaining', 'created_at', 'updated_at'
    ]

    list_filter = ['organization_name', 'initiative', 'resource_type']
    search_fields = ['resource_name', 'resource_type', 'initiative__initiative_name']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at', 'resource_remaining']

    # Filter foreign keys by logged-in user's organization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_name'):
            org = request.user.organization_name
            if db_field.name == 'initiative':
                kwargs['queryset'] = Initiative.objects.filter(organization_name=org)
            if db_field.name == 'organization_name':
                kwargs['queryset'] = OrganizationalProfile.objects.filter(pk=org.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Restrict queryset to user's organization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'organization_name') and request.user.organization_name:
            return qs.filter(organization_name=request.user.organization_name)
        return qs.none()

    # Pass request to form for filtering initiative dropdown
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['request'] = request
        return form_kwargs