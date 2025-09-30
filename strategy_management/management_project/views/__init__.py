# views/__init__.py
from .dashboard import dashboard

from .swot_analysis import swot_analysis_list, create_swot_analysis, update_swot_analysis, delete_swot_analysis, \
    export_swot_analysis_to_excel, swot_analysis_chart

from .vision import vision_list, create_vision, update_vision, delete_vision
from .mission import mission_list, create_mission, update_mission, delete_mission
from .values import values_list, create_values, update_values, delete_values

from .strategy_hierarchy import strategy_hierarchy_list, create_strategy_hierarchy, update_strategy_hierarchy, delete_strategy_hierarchy

from .department import department_list, create_department, update_department, delete_department

from .stakeholder import  stakeholder_list, create_stakeholder, update_stakeholder, delete_stakeholder, \
    export_stakeholders_to_excel, stakeholder_graph_view

from .organization import organizational_profile, create_organizational_profile, update_organizational_profile, \
    delete_organizational_profile

from .strategic_cycle import strategic_cycle_list, create_strategic_cycle, \
    update_strategic_cycle, delete_strategic_cycle

from .strategic_action_plan import strategic_action_plan_by_cycle, strategic_action_plan_list, strategic_action_plan_detail, \
    create_strategic_action_plan, update_strategic_action_plan, delete_strategic_action_plan, \
    export_strategic_action_plan_to_excel, strategic_action_plan_chart

from .strategic_report import strategy_report_by_cycle_list, strategic_report_detail, strategic_report_list, \
    create_strategic_report, update_strategic_report, delete_strategic_report, \
    export_strategic_report_to_excel, strategic_report_chart


from .swot_report import swot_report_by_cycle_list, swot_report_list, \
    create_swot_report, update_swot_report, delete_swot_report, swot_report_chart

from .initiative import  initiative_list, create_initiative, update_initiative, delete_initiative, \
    export_initiative_to_excel, initiative_chart

from .initiative_timeline import initiative_timeline_list, create_initiative_timeline, \
    update_initiative_timeline, delete_initiative_timeline

# Initiative Budget
from .initiative_budget import initiative_budget_list, create_initiative_budget, \
    update_initiative_budget, delete_initiative_budget

# Initiative Resource
from .initiative_resource import initiative_resource_list, create_initiative_resource, \
    update_initiative_resource, delete_initiative_resource


