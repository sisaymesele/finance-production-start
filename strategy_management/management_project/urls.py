from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # organizational_profile
    path('organizational-profile/', views.organizational_profile, name='organizational_profile'),
    path('organizational-profile/create/', views.create_organizational_profile, name='create_organizational_profile'),
    path('organizational-profile/update/<int:pk>/', views.update_organizational_profile, name='update_organizational_profile'),
    path('organizational-profile/delete/<int:pk>/', views.delete_organizational_profile, name='delete_organizational_profile'),

    # SWOT
    path('swot_analysis/', views.swot_analysis_list, name='swot_analysis_list'),
    path('swot_analysis/create/', views.create_swot_analysis, name='create_swot_analysis'),
    path('swot_analysis/update/<int:pk>/', views.update_swot_analysis, name='update_swot_analysis'),
    path('swot_analysis/delete/<int:pk>/', views.delete_swot_analysis, name='delete_swot_analysis'),

    # Vision
    path('vision/', views.vision_list, name='vision_list'),
    path('vision/create/', views.create_vision, name='create_vision'),
    path('vision/update/<int:pk>/', views.update_vision, name='update_vision'),
    path('vision/delete/<int:pk>/', views.delete_vision, name='delete_vision'),

    # Mission
    path('mission/', views.mission_list, name='mission_list'),
    path('mission/create/', views.create_mission, name='create_mission'),
    path('mission/update/<int:pk>/', views.update_mission, name='update_mission'),
    path('mission/delete/<int:pk>/', views.delete_mission, name='delete_mission'),

    # Values
    path('values/', views.values_list, name='values_list'),
    path('values/create/', views.create_values, name='create_values'),
    path('values/update/<int:pk>/', views.update_values, name='update_values'),
    path('values/delete/<int:pk>/', views.delete_values, name='delete_values'),

    # Strategy Hierarchy URLs
    path('strategy-hierarchy/', views.strategy_hierarchy_list, name='strategy_hierarchy_list'),
    path('strategy-hierarchy/create/', views.create_strategy_hierarchy, name='create_strategy_hierarchy'),
    path('strategy-hierarchy/<int:pk>/update/', views.update_strategy_hierarchy, name='update_strategy_hierarchy'),
    path('strategy-hierarchy/<int:pk>/delete/', views.delete_strategy_hierarchy, name='delete_strategy_hierarchy'),

    # View the stakeholder_list list
# Stakeholder List & Search
    path('stakeholders/', views.stakeholder_list, name='stakeholder_list'),
    # Export Stakeholders to Excel
    path('stakeholders/export/', views.export_stakeholders_to_excel, name='export_stakeholders_to_excel'),
    # Create update a Stakeholder
    path('stakeholders/create/', views.create_stakeholder, name='create_stakeholder'),
    path('stakeholders/update/<int:pk>/', views.update_stakeholder, name='update_stakeholder'),
    path('stakeholders/delete/<int:pk>/', views.delete_stakeholder, name='delete_stakeholder'),
    # Stakeholder Graph / Analytics View
    path('stakeholders/graph/', views.stakeholder_graph_view, name='stakeholder_graph'),


    # payroll month component
    path('strategic-cycle/', views.strategic_cycle_list, name='strategic_cycle_list'),
    path('strategic-cycle/create/', views.create_strategic_cycle, name='create_strategic_cycle'),
    path('strategic-cycle/update/<int:pk>/', views.update_strategic_cycle, name='update_strategic_cycle'),
    path('strategic-cycle/delete/<int:pk>/', views.delete_strategic_cycle, name='delete_strategic_cycle'),

    ## Strategic Report URLs
    # List all cycles for reports
    path('strategy-report-by-cycle/', views.strategy_report_by_cycle_list, name='strategy_report_by_cycle_list'),

    # List reports by cycle
    path('strategy-report/<slug:cycle_slug>/', views.strategic_report_list, name='strategic_report_list'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/', views.strategic_report_detail, name='strategic_report_detail'),

    # CRUD
    path('strategy-report/<slug:cycle_slug>/create/', views.create_strategic_report, name='create_strategic_report'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/update/', views.update_strategic_report, name='update_strategic_report'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/delete/', views.delete_strategic_report, name='delete_strategic_report'),
    #export excel
    path('strategic-reports/export/<slug:cycle_slug>/', views.export_strategic_report_to_excel, name='export_strategic_report'),
    path('strategic-report/chart/', views.strategic_report_chart, name='strategic_report_chart'),


    #action plan
    # Strategic Action Plan Chart
    path( 'strategic-action-plan/chart/', views.strategic_action_plan_chart, name='strategic_action_plan_chart'),
    path('strategic-action-plan-by-cycle/', views.strategic_action_plan_by_cycle, name='strategic_action_plan_by_cycle'),
    path('strategic-action-plan/<slug:cycle_slug>/', views.strategic_action_plan_list, name='strategic_action_plan_list'),
    path( 'strategic-action-plan/<slug:slug>/', views.strategic_action_plan_detail, name='strategic_action_plan_detail'),
    path( 'management-project/strategic-action-plan/<slug:cycle_slug>/<int:pk>/', views.strategic_action_plan_detail, name='strategic_action_plan_detail'),

    # path('strategic-action-plan/<slug:cycle_slug>/<int:pk>/', views.strategic_action_plan_detail, name='strategic_action_plan_detail'),
    path('strategic-action-plan/<slug:cycle_slug>/create/', views.create_strategic_action_plan, name='create_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/update/<int:pk>/', views.update_strategic_action_plan, name='update_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/delete/<int:pk>/', views.delete_strategic_action_plan, name='delete_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/export/', views.export_strategic_action_plan_to_excel, name='export_strategic_action_plan_to_excel'),

    # Swot Report URLs
    # List all cycles with swot reports
    # Cycle list
    # ---------------- CYCLE LIST ----------------
    path('swot-report/', views.swot_report_list, name='swot_report_list'),
    path('swot-report/create/', views.create_swot_report, name='create_swot_report'),
    path('swot-report/update/<int:pk>/', views.update_swot_report, name='update_swot_report'),
    path('swot-report/delete/<int:pk>/', views.delete_swot_report, name='delete_swot_report'),

    # # List all cycles (entry point)
    path('swot-report-by-cycle/', views.swot_report_by_cycle_list, name='swot_report_by_cycle_list'),
    #
    # path('swot/<slug:cycle_slug>/', views.swot_report_list, name='swot_report_list'),
    # path('swot/<slug:cycle_slug>/create/', views.create_swot_report, name='create_swot_report'),
    # path('swot/<slug:cycle_slug>/<int:pk>/update/', views.update_swot_report, name='update_swot_report'),
    # path('swot/<slug:cycle_slug>/<int:pk>/delete/', views.delete_swot_report, name='delete_swot_report'),





]
