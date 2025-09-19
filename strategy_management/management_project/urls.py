from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # organizational_profile
    path('organizational-profile/', views.organizational_profile, name='organizational_profile'),
    path('organizational-profile/create/', views.create_organizational_profile, name='create_organizational_profile'),
    path('organizational-profile/update/<int:pk>/', views.update_organizational_profile, name='update_organizational_profile'),
    path('organizational-profile/delete/<int:pk>/', views.delete_organizational_profile, name='delete_organizational_profile'),

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

    # payroll period URLs
    path('payroll-period/', views.payroll_period_list, name='payroll_period_list'),
    path('payroll-period/create/', views.create_payroll_period, name='create_payroll_period'),
    path('payroll-period/update/<int:pk>/', views.update_payroll_period, name='update_payroll_period'),
    path('payroll-period/delete/<int:pk>/', views.delete_payroll_period, name='delete_payroll_period'),

    # payroll month component
    path('strategic-cycle/', views.strategic_cycle_list, name='strategic_cycle_list'),
    path('strategic-cycle/create/', views.create_strategic_cycle, name='create_strategic_cycle'),
    path('strategic-cycle/update/<int:pk>/', views.update_strategic_cycle, name='update_strategic_cycle'),
    path('strategic-cycle/delete/<int:pk>/', views.delete_strategic_cycle, name='delete_strategic_cycle'),

    ## Strategic Report URLs
    path('strategic-reports/', views.strategic_report_list, name='strategic_report_list'),
    path('strategic-reports/create/', views.create_strategic_report, name='create_strategic_report'),
    path('strategic-reports/<int:pk>/update/', views.update_strategic_report, name='update_strategic_report'),
    path('strategic-reports/<int:pk>/delete/', views.delete_strategic_report, name='delete_strategic_report'),
    path('strategic-reports/chart/', views.strategic_report_chart, name='strategic_report_chart'),
    path(
        'strategic-reports/export/',
        views.export_strategic_report_to_excel,
        name='export_strategic_report_to_excel'
    ),

    #total

    #

    # urls.py for DeductionAdjustment
    path('deduction-adjustment/list', views.deduction_object_list, name='deduction_adjustment_list'),
    path('deduction-adjustment/detail', views.deduction_object_detail, name='deduction_adjustment_detail'),
    path('deduction-adjustment/per-adjusted-month/', views.deduction_per_adjusted_month, name='deduction_per_adjusted_month'),
    path('deduction-adjustment/monthly-adjustment/', views.monthly_deduction_adjustment, name='monthly_deduction_adjustment'),
    path('deduction-adjustment/create/', views.create_deduction_adjustment, name='create_deduction_adjustment'),
    path('deduction-adjustment/update/<int:pk>/', views.update_deduction_adjustment, name='update_deduction_adjustment'),
    path('deduction-adjustment/delete/<int:pk>/', views.delete_deduction_adjustment, name='delete_deduction_adjustment'),
    #total
    path('monthly-deduction-adjustment-total', views.monthly_deduction_adjustment_total, name='monthly_deduction_adjustment_total'),

    #export
    path('export-deduction-adjustment/', views.export_deduction_adjustment_list_to_excel, name='export_deduction_adjustment_list_to_excel'),
    path('export-deduction-per-adjusted-month/', views.export_deduction_per_adjusted_month_to_excel, name='export_deduction_per_adjusted_month_to_excel'),
    path('export-monthly-deduction-adjustment/', views.export_monthly_deduction_adjustment_to_excel, name='export_monthly_deduction_adjustment_to_excel'),
    path('export_monthly_deduction_adjustment_aggregate', views.export_monthly_deduction_adjustment_aggregate, name='export_monthly_deduction_adjustment_aggregate'),

    #
    # combined personnel
    path('combined-personnel-detail/', views.combined_personnel_detail, name='combined_personnel_detail'),
    path('combined-personnel-adjustment/', views.combined_personnel_adjustment_list, name='combined_personnel_adjustment'),
    path('combined-personnel-payroll/', views.combined_personnel_payroll_list, name='combined_personnel_payroll'),
    path('combined-personnel-total/', views.combined_personnel_total, name='combined_personnel_total'),
    path('combined-personnel-expense/', views.combined_personnel_expense, name='combined_personnel_expense'),
    path('combined-personnel-net-income/', views.combined_personnel_net_income, name='combined_personnel_net_income'),
    path('combined-personnel-employment-income-tax/', views.combined_personnel_employment_income_tax, name='combined_personnel_employment_income_tax'),
    path('combined-personnel-pension/', views.combined_employee_pension, name='combined_personnel_pension'),
    #export
    path('export-combined-personnel-detail/', views.export_combined_personnel_detail, name='export_combined_personnel_detail'),

    path('combined-personnel-list/export/', views.export_combined_personnel_list, name='export_combined_personnel_list'),
    path('export-combined-payroll-expense/', views.export_combined_personnel_expense, name='export_combined_personnel_expense'),
    path('export-combined-net-income/', views.export_combined_personnel_net_income, name='export_combined_personnel_net_income'),
    path('export-combined-employment-tax/', views.export_combined_personnel_employment_tax, name='export_combined_personnel_employment_tax'),
    path('export-combined-personnel-pension/', views.export_combined_personnel_pension, name='export_combined_personnel_pension'),
    path('export-total-adjustment/', views.export_personnel_total_adjustment, name='export_personnel_total_adjustment'),
    path('combined-total-payroll/export/', views.export_combined_personnel_total, name='export_combined_personnel_total'),

    #combined monthly and yearly
    path('combined-monthly-detail/', views.monthly_combined_detail, name='combined_monthly_detail'),
    path('combined-monthly-summary/', views.monthly_combined_summary, name='combined_monthly_summary'),

    #yearly
    path('combined-yearly-detail/', views.yearly_combined_detail_view, name='combined_yearly_detail'),
    path('combined-yearly-summary/', views.yearly_combined_summary_view, name='combined_yearly_summary'),

    #export
    path('export-combined-monthly-detail/', views.export_combined_monthly_detail_to_excel, name='export_combined_monthly_detail_to_excel'),
    path('export-combined-monthly-summary/', views.export_combined_monthly_summary_to_excel, name='export_combined_monthly_summary_to_excel'),
    path('export-combined-yearly-summary/', views.export_combined_yearly_summary_to_excel,name='export_combined_yearly_summary_to_excel'),

    path('combined-yearly-detail/export/', views.export_combined_yearly_detail_to_excel,name='export_combined_yearly_detail_to_excel'),
    #graph
    path('combined-monthly-graph/', views.combined_monthly_graph_view, name='combined_monthly_graph'),

    #

    # severance pay
    path('severance-pay/', views.severance_pay_list, name='severance-pay-list'),
    path('export-severance-pay-to-excel/', views.export_severance_pay_to_excel, name='export_severance_pay_to_excel'),
    path('severance-pay/<int:pk>/', views.severance_pay_detail, name='severance_pay_detail'),
    path('severance-pay/create/', views.create_severance_pay, name='create_severance_pay'),
    path('severance-pay/update/<int:pk>/', views.update_severance_pay, name='update_severance_pay'),
    path('severance-pay/delete/<int:pk>/', views.delete_severance_pay, name='delete_severance_pay'),
    path('severance-pay-summary/', views.severance_pay_report, {'template_name': 'severance_pay/summary.html'}, name='severance_pay_summary'),
    path('severance-pay-journal-entry/', views.severance_pay_report, {'template_name': 'severance_pay/journal_entry.html'}, name='severance_pay_journal_entry'),

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

    # SWOT
    path('swot/', views.swot_list, name='swot_list'),
    path('swot/create/', views.create_swot, name='create_swot'),
    path('swot/update/<int:pk>/', views.update_swot, name='update_swot'),
    path('swot/delete/<int:pk>/', views.delete_swot, name='delete_swot'),

    # Strategy Map URLs
    path('strategy-map/', views.strategy_map_list, name='strategy_map_list'),
    path('strategy-map/create/', views.create_strategy_map, name='create_strategy_map'),
    path('strategy-map/<int:pk>/update/', views.update_strategy_map, name='update_strategy_map'),
    path('strategy-map/<int:pk>/delete/', views.delete_strategy_map, name='delete_strategy_map'),

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
        "management-project/strategic-action-plan/<slug:cycle_slug>/<int:pk>/",
        views.strategic_action_plan_detail,
        name="strategic_action_plan_detail"
    ),


    # path('strategic-action-plan/<slug:cycle_slug>/<int:pk>/', views.strategic_action_plan_detail, name='strategic_action_plan_detail'),
    path('strategic-action-plan/<slug:cycle_slug>/create/', views.create_strategic_action_plan, name='create_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/update/<int:pk>/', views.update_strategic_action_plan, name='update_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/delete/<int:pk>/', views.delete_strategic_action_plan, name='delete_strategic_action_plan'),
    path('strategic-action-plan/<slug:cycle_slug>/export/', views.export_strategic_action_plan_to_excel, name='export_strategic_action_plan_to_excel'),


]
