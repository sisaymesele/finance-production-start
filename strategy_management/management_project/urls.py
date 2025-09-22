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
    path('swot/', views.swot_list, name='swot_list'),
    path('swot/create/', views.create_swot, name='create_swot'),
    path('swot/update/<int:pk>/', views.update_swot, name='update_swot'),
    path('swot/delete/<int:pk>/', views.delete_swot, name='delete_swot'),

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

    # Strategy Map URLs
    path('strategy-map/', views.strategy_map_list, name='strategy_map_list'),
    path('strategy-map/create/', views.create_strategy_map, name='create_strategy_map'),
    path('strategy-map/<int:pk>/update/', views.update_strategy_map, name='update_strategy_map'),
    path('strategy-map/<int:pk>/delete/', views.delete_strategy_map, name='delete_strategy_map'),

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
    path('strategy-report/', views.strategy_report_by_cycle_list, name='strategy_report_by_cycle_list'),

    # List reports by cycle
    path('strategy-report/<slug:cycle_slug>/', views.strategic_report_list, name='strategic_report_list'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/', views.strategic_report_detail, name='strategic_report_detail'),

    # CRUD
    path('strategy-report/<slug:cycle_slug>/create/', views.create_strategic_report, name='create_strategic_report'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/update/', views.update_strategic_report, name='update_strategic_report'),
    path('strategy-report/<slug:cycle_slug>/<int:pk>/delete/', views.delete_strategic_report, name='delete_strategic_report'),
    #export excel
    path('strategic-reports/export/<slug:cycle_slug>/', views.export_strategic_report_to_excel, name='export_strategic_reports'),
    path('strategic-report/chart/', views.strategic_report_chart, name='strategic_report_chart'),


    #action plan
    # Strategic Action Plan Chart
    path(
        'strategic-action-plan/chart/',
        views.strategic_action_plan_chart,
        name='strategic_action_plan_chart'
    ),
    path('strategy-by-cycle/', views.strategy_by_cycle_list, name='strategy_by_cycle_list'),
    path('strategic-action-plan/<slug:cycle_slug>/', views.strategic_action_plan_list, name='strategic_action_plan_list'),
    path(
        "strategic-action-plan/<slug:slug>/",
        views.strategic_action_plan_detail,
        name="strategic_action_plan_detail"
    ),

    path(
        'management-project/strategic-action-plan/<slug:cycle_slug>/<int:pk>/',
        views.strategic_action_plan_detail,
        name='strategic_action_plan_detail'
    ),


    # path('strategic-action-plan/<slug:cycle_slug>/<int:pk>/', views.strategic_action_plan_detail, name='strategic_action_plan_detail'),
    path('strategic-action-plan/<slug:cycle_slug>/create/', views.create_strategic_action_plan, name='create_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/update/<int:pk>/', views.update_strategic_action_plan, name='update_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/delete/<int:pk>/', views.delete_strategic_action_plan, name='delete_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/export/', views.export_strategic_action_plan_to_excel, name='export_strategic_action_plan_to_excel'),


]
