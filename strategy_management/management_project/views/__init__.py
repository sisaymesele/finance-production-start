# views/__init__.py
from .dashboard import dashboard

from .stakeholder import  stakeholder_list, create_stakeholder, update_stakeholder, delete_stakeholder, \
    export_stakeholders_to_excel, stakeholder_graph_view

from .organization import organizational_profile, create_organizational_profile, update_organizational_profile, \
    delete_organizational_profile

from .payroll_period import payroll_period_list, create_payroll_period, \
    update_payroll_period, delete_payroll_period

from .strategic_cycle import strategic_cycle_list, create_strategic_cycle, \
    update_strategic_cycle, delete_strategic_cycle

from .strategic_action_plan import strategy_by_cycle_list, strategic_action_plan_list, strategic_action_plan_detail, \
    create_strategic_action_plan, update_strategic_action_plan, delete_strategic_action_plan, \
    export_strategic_action_plan_to_excel, strategic_action_plan_chart

from .strategic_report import strategic_report_list, \
    create_strategic_report, update_strategic_report, delete_strategic_report, \
    export_strategic_report_to_excel, strategic_report_chart

from .deduction_adjustment import deduction_object_list, deduction_object_detail, \
    create_deduction_adjustment, update_deduction_adjustment, delete_deduction_adjustment, deduction_per_adjusted_month, \
    monthly_deduction_adjustment, monthly_deduction_adjustment_total, export_deduction_adjustment_list_to_excel, \
    export_deduction_per_adjusted_month_to_excel, export_monthly_deduction_adjustment_to_excel, \
    export_monthly_deduction_adjustment_aggregate

from .combined_personnel import get_combined_personnel_payroll_context, combined_personnel_payroll_list, \
    combined_personnel_adjustment_list, combined_personnel_total, combined_personnel_expense, combined_personnel_net_income, \
    combined_employee_pension, combined_personnel_employment_income_tax, export_combined_personnel_list, export_personnel_total_adjustment, \
    export_combined_personnel_total, export_combined_personnel_expense, \
    export_combined_personnel_net_income, export_combined_personnel_employment_tax, export_combined_personnel_pension, \
    combined_personnel_detail, export_combined_personnel_detail

from .combined_monthly import get_combined_monthly_detail, monthly_combined_detail, \
    export_combined_monthly_detail_to_excel, combined_monthly_graph_view, \
    monthly_combined_summary, export_combined_monthly_summary_to_excel

from .combined_yearly import get_combined_yearly_detail, yearly_combined_detail_view, \
    export_combined_yearly_detail_to_excel, yearly_combined_summary_view, export_combined_yearly_summary_to_excel

from .severance_pay import severance_pay_list,  severance_pay_detail, create_severance_pay, update_severance_pay, \
    delete_severance_pay, severance_pay_report, export_severance_pay_to_excel

from .vision import vision_list, create_vision, update_vision, delete_vision
from .mission import mission_list, create_mission, update_mission, delete_mission
from .values import values_list, create_values, update_values, delete_values
from .swot import swot_list, create_swot, update_swot, delete_swot
from .strategy_map import strategy_map_list, create_strategy_map, update_strategy_map, delete_strategy_map
