# views/__init__.py
from .dashboard import dashboard

from .stakeholder import  stakeholder_list, create_stakeholder, update_stakeholder, delete_stakeholder, \
    export_stakeholders_to_excel, stakeholder_graph_view

from .organization import organizational_profile, create_organizational_profile, update_organizational_profile, \
    delete_organizational_profile

from .strategic_cycle import strategic_cycle_list, create_strategic_cycle, \
    update_strategic_cycle, delete_strategic_cycle

from .strategic_action_plan import strategy_by_cycle_list, strategic_action_plan_list, strategic_action_plan_detail, \
    create_strategic_action_plan, update_strategic_action_plan, delete_strategic_action_plan, \
    export_strategic_action_plan_to_excel, strategic_action_plan_chart

from .strategic_report import strategy_report_by_cycle_list, strategic_report_detail, strategic_report_list, \
    create_strategic_report, update_strategic_report, delete_strategic_report, \
    export_strategic_report_to_excel, strategic_report_chart

from .vision import vision_list, create_vision, update_vision, delete_vision
from .mission import mission_list, create_mission, update_mission, delete_mission
from .values import values_list, create_values, update_values, delete_values
from .swot import swot_list, create_swot, update_swot, delete_swot
from .strategy_map import strategy_map_list, create_strategy_map, update_strategy_map, delete_strategy_map
