# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db import transaction
# from django.db.models import Q
#
# from management_project.models import (
#     StrategicActionPlan, StrategicReport, DeductionAdjustment
# )
# from management_project.services.strategic_report.business import StrategicReportBusinessService
# from management_project.services.deduction_adjustment.business import DeductionAdjustmentBusinessService
#
# # -------------------------------
# # Strategic Report Recalculations
# # -------------------------------
#
# def _recalc_strategic_report(instance):
#     service = StrategicReportBusinessService(instance=instance)
#     service.calculate_strategic_report_per_adjusted_month()
#     service.calculate_monthly_strategic_report()
#
# @receiver(post_save, sender=StrategicActionPlan)
# def recalc_adjustments_on_strategic_action_plan_save(sender, instance, **kwargs):
#     def _recalc_all():
#         adjustments = StrategicReport.objects.filter(
#             Q(payroll_to_record=instance) | Q(payroll_needing_adjustment=instance)
#         )
#         for adj in adjustments:
#             _recalc_strategic_report(adj)
#
#     transaction.on_commit(_recalc_all)
#
# @receiver(post_save, sender=StrategicReport)
# def recalc_strategic_action_plan_on_adjustment_save(sender, instance, **kwargs):
#     if instance.payroll_to_record:
#         transaction.on_commit(lambda: _recalc_strategic_report(instance))
#
# @receiver(post_delete, sender=StrategicReport)
# def recalc_strategic_action_plan_on_adjustment_delete(sender, instance, **kwargs):
#     if instance.payroll_to_record:
#         _recalc_strategic_report(instance)
#
# # -------------------------------
# # Deduction Adjustment Recalculations
# # -------------------------------
#
# def _recalc_deduction_adjustment(instance):
#     service = DeductionAdjustmentBusinessService(instance=instance)
#     service.calculate_deduction_adjustment_per_adjusted_month()
#     service.calculate_monthly_deduction_adjustment()
#
# @receiver(post_save, sender=DeductionAdjustment)
# def recalc_deductions_on_save(sender, instance, **kwargs):
#     transaction.on_commit(lambda: _recalc_deduction_adjustment(instance))
#
# @receiver(post_delete, sender=DeductionAdjustment)
# def recalc_deductions_on_delete(sender, instance, **kwargs):
#     _recalc_deduction_adjustment(instance)
#
# #
