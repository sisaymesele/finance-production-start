from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from management_project.models import StrategicReport, StrategicActionPlan
from management_project.forms import StrategicReportForm
from management_project.models import StrategicActionPlan

@login_required
def strategic_report_list(request):
    """
    List all strategic reports for the logged-in user's organization,
    with optional search, Strategic Cycle filter, Responsible Body filter,
    and pagination. Works with or without HTMX.
    """
    org = request.user.organization_name
    reports = StrategicReport.objects.filter(
        organization_name=org
    ).select_related('action_plan', 'action_plan__strategic_cycle').prefetch_related('action_plan__responsible_bodies')

    # --- Dropdown filters ---
    cycle_id = request.GET.get('cycle')
    responsible_body = request.GET.get('responsible_body')

    if cycle_id:
        reports = reports.filter(action_plan__strategic_cycle_id=cycle_id)
    if responsible_body:
        reports = reports.filter(action_plan__responsible_bodies__stakeholder_name=responsible_body)

    # --- Search filter ---
    search_query = request.GET.get('search', '').strip()
    if search_query:
        reports = reports.filter(
            Q(action_plan__strategy_map__kpi__icontains=search_query) |
            Q(action_plan__strategy_map__objective__icontains=search_query) |
            Q(action_plan__strategy_map__strategic_pillar__icontains=search_query) |
            Q(action_plan__strategy_map__strategic_perspective__icontains=search_query)
        )

    # --- Remove duplicates from ManyToMany filtering ---
    reports = reports.distinct()

    # --- Pagination ---
    paginator = Paginator(reports, 10)  # 10 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Get dropdown options ---
    cycles = StrategicCycle.objects.filter(organization_name=org)
    responsible_bodies = set()
    for report in reports:
        responsible_bodies.update([b.stakeholder_name for b in report.action_plan.responsible_bodies.all()])
    responsible_bodies = sorted(responsible_bodies)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'cycles': cycles,
        'responsible_bodies': responsible_bodies,
        'selected_cycle': int(cycle_id) if cycle_id else None,
        'selected_body': responsible_body,
    }

    template_name = 'strategic_report/list.html'
    if request.headers.get('HX-Request'):  # HTMX request
        template_name = 'strategic_report/list_partial.html'

    return render(request, template_name, context)


# @login_required
# def strategic_report_list(request):
#     """
#     List all strategic reports for the logged-in user's organization,
#     with optional search and pagination.
#     """
#     org = request.user.organization_name
#     reports = StrategicReport.objects.filter(organization_name=org).select_related('action_plan')
#
#     # Search filter
#     search_query = request.GET.get('search', '').strip()
#     if search_query:
#         reports = reports.filter(
#             Q(action_plan__strategy_map__kpi__icontains=search_query) |
#             Q(action_plan__strategy_map__objective__icontains=search_query) |
#             Q(action_plan__strategy_map__kpi__icontains=search_query) |
#             Q(action_plan__strategy_map__strategic_pillar__icontains=search_query) |
#             Q(action_plan__strategy_map__strategic_perspective__icontains=search_query) |
#             Q(action_plan__responsible_body__icontains=search_query)
#         )
#
#     # Pagination
#     paginator = Paginator(reports, 10)  # 10 reports per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_obj,
#         'search_query': search_query,
#     }
#     return render(request, 'strategic_report/list.html', context)
# #

@login_required
def create_strategic_report(request):
    if request.method == 'POST':
        form = StrategicReportForm(request.POST, request=request)
        if form.is_valid():
            strategic_report = form.save(commit=False)
            strategic_report.organization_name = request.user.organization_name
            strategic_report.save()
            messages.success(request, "Strategic Report created successfully!")
            return redirect('strategic_report_list')
        else:
            messages.error(request, "Error creating the strategic report. Check the form.")
    else:
        form = StrategicReportForm(request=request)

    context = {
        'form': form,
        'form_title': 'Create Strategic Report',
        'submit_button_text': 'Create Strategic Report',
    }
    return render(request, 'strategic_report/form.html', context)

@login_required
def update_strategic_report(request, pk):
    strategic_report = get_object_or_404(
        StrategicReport, pk=pk, organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = StrategicReportForm(request.POST, instance=strategic_report, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Strategic Report updated successfully!")
            return redirect('strategic_report_list')
        else:
            messages.error(request, "Error updating the strategic report. Check the form.")
    else:
        form = StrategicReportForm(instance=strategic_report, request=request)

    context = {
        'form': form,
        'form_title': 'Update Strategic Report',
        'submit_button_text': 'Update Strategic Report',
    }
    return render(request, 'strategic_report/form.html', context)

@login_required
def delete_strategic_report(request, pk):
    # Fetch the payroll entry to delete
    strategic_report = get_object_or_404(StrategicReport, pk=pk, organization_name=request.user.organization_name)

    if request.method == "POST":
        strategic_report.delete()
        messages.success(request, "Strategic Report deleted successfully!")
        return redirect('strategic_report_list')

    context = {'strategic_report': strategic_report}

    return render(request, 'strategic_report/delete_confirm.html', context)

#export
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from io import BytesIO
from management_project.models import StrategicReport

def split_two_lines(text):
    """Split a long text roughly into two lines."""
    if not text:
        return ""
    words = text.split()
    mid = len(words) // 2
    return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

@login_required
def export_strategic_report_to_excel(request):
    # Get all reports for the user's organization
    reports = StrategicReport.objects.filter(
        organization_name=request.user.organization_name
    ).select_related('action_plan', 'action_plan__strategic_cycle')

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Strategic Reports"

    # Title row
    title_text = "Strategic Reports"
    sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=20)
    title_cell = sheet.cell(row=1, column=1, value=title_text)
    title_cell.font = Font(bold=True, size=14, color="FFFFFF")
    title_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    title_cell.fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    title_cell.border = Border(
        left=Side(border_style="thin"),
        right=Side(border_style="thin"),
        top=Side(border_style="thin"),
        bottom=Side(border_style="thin")
    )

    # Column headers
    headers = [
        "#", "Time Horizon", "Time Horizon Type", "Start Date", "End Date", "KPI",
        "Baseline", "Target", "Achievement", "Percent Achieved", "Variance", "Weighted Score",
        "Responsible Body", "Data Source", "Data Collector", "Progress Summary",
        "Performance Summary", "Status", "Created At", "Updated At"
    ]
    for col_num, header in enumerate(headers, start=1):
        cell = sheet.cell(row=2, column=col_num, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.fill = PatternFill(start_color="4BACC6", end_color="4BACC6", fill_type="solid")
        cell.border = Border(
            left=Side(border_style="thin"),
            right=Side(border_style="thin"),
            top=Side(border_style="thin"),
            bottom=Side(border_style="thin")
        )

    # Data rows
    for row_idx, report in enumerate(reports, start=3):
        plan = report.action_plan
        cycle_obj = plan.strategic_cycle
        data = [
            row_idx - 2,
            cycle_obj.time_horizon if cycle_obj else "",
            cycle_obj.time_horizon_type if cycle_obj else "",
            cycle_obj.start_date.strftime('%B %d, %Y') if cycle_obj and cycle_obj.start_date else "",
            cycle_obj.end_date.strftime('%B %d, %Y') if cycle_obj and cycle_obj.end_date else "",
            split_two_lines(plan.strategy_map.kpi),
            plan.baseline,
            plan.target,
            report.achievement,
            report.percent_achieved,
            report.variance,
            report.weighted_score,
            ", ".join([b.stakeholder_name for b in plan.responsible_bodies.all()]),
            report.data_source or "",
            report.data_collector or "",
            split_two_lines(report.progress_summary),
            split_two_lines(report.performance_summary),
            report.status,
            report.created_at.strftime('%Y-%m-%d %H:%M'),
            report.updated_at.strftime('%Y-%m-%d %H:%M')
        ]

        for col_num, value in enumerate(data, start=1):
            cell = sheet.cell(row=row_idx, column=col_num, value=value)
            if col_num in [6, 13, 16, 17]:  # Wrap KPI, Responsible Body, Progress, Performance
                cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = Border(
                left=Side(border_style="thin"),
                right=Side(border_style="thin"),
                top=Side(border_style="thin"),
                bottom=Side(border_style="thin")
            )

    # Adjust column widths
    min_width = 10
    max_width = 25
    for col_idx in range(1, sheet.max_column + 1):
        width = min_width
        for row_idx in range(2, sheet.max_row + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            if cell.value:
                width = max(width, min(len(str(cell.value)) + 2, max_width))
        sheet.column_dimensions[get_column_letter(col_idx)].width = width

    # Save to buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Strategic_Reports.xlsx"'
    return response




# views.py

from django.shortcuts import render
from django.db.models import Avg, Count
from management_project.models import StrategicReport, StrategicCycle
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from datetime import datetime
from collections import defaultdict


def strategic_report_chart(request):
    # ---------------- Filters ----------------
    cycle_filter = request.GET.get("strategic_cycle", "all")
    body_filter = request.GET.get("responsible_body", "all")
    horizon_filter = request.GET.get("time_horizon", "all")

    reports = StrategicReport.objects.select_related(
        "action_plan", "action_plan__strategic_cycle", "organization_name"
    ).prefetch_related("action_plan__responsible_bodies")

    if cycle_filter != "all":
        reports = reports.filter(action_plan__strategic_cycle_id=cycle_filter)
    if body_filter != "all":
        reports = reports.filter(action_plan__responsible_bodies__stakeholder_name=body_filter)
    if horizon_filter != "all":
        reports = reports.filter(action_plan__strategic_cycle__time_horizon_type=horizon_filter)

    # ---------------- 1. Summary Stats (Box) ----------------
    total_reports = reports.count()
    avg_percent_achieved = reports.aggregate(avg=Avg("percent_achieved"))["avg"] or 0
    avg_variance = reports.aggregate(avg=Avg("variance"))["avg"] or 0
    avg_weighted_score = reports.aggregate(avg=Avg("weighted_score"))["avg"] or 0

    # ---------------- 2. Status Pie Chart ----------------
    status_counts = reports.values("status").annotate(count=Count("id"))
    status_map = {
        "pending": {"name": "Pending", "color": "#FFCE56"},
        "in_progress": {"name": "In Progress", "color": "#36A2EB"},
        "completed": {"name": "Completed", "color": "#4BC0C0"},
        "on_hold": {"name": "On Hold", "color": "#FF6384"},
        "cancelled": {"name": "Cancelled", "color": "#9966FF"},
    }
    if status_counts:
        status_fig = go.Figure(
            data=[
                go.Pie(
                    labels=[status_map[i["status"]]["name"] for i in status_counts],
                    values=[i["count"] for i in status_counts],
                    hole=0.3,
                    marker=dict(colors=[status_map[i["status"]]["color"] for i in status_counts]),
                    textinfo="percent+label",
                )
            ]
        )
        status_fig.update_layout(title_text="Report Status Distribution")
        status_plot = plot(status_fig, output_type="div", config={"displayModeBar": False})
    else:
        status_plot = "<div class='no-data'>No status data available</div>"

    # ---------------- 4. Metrics by Responsible Body + Cycle ----------------
    cycle_data = (
        reports.values("action_plan__strategic_cycle__end_date")
        .annotate(
            avg_percent_achieved=Avg("percent_achieved"),
            avg_variance=Avg("variance"),
            avg_weighted_score=Avg("weighted_score"),
        )
        .order_by("action_plan__strategic_cycle__end_date")
    )

    cycle_dates = [
        c["action_plan__strategic_cycle__end_date"].strftime("%B %Y") if c["action_plan__strategic_cycle__end_date"] else "N/A"
        for c in cycle_data
    ]
    cycle_fig = go.Figure()
    cycle_fig.add_trace(go.Bar(name="Percent Achieved", x=cycle_dates, y=[c["avg_percent_achieved"] or 0 for c in cycle_data], marker_color="#4BC0C0"))
    cycle_fig.add_trace(go.Bar(name="Variance", x=cycle_dates, y=[c["avg_variance"] or 0 for c in cycle_data], marker_color="#FF6384"))
    cycle_fig.add_trace(go.Bar(name="Weighted Score", x=cycle_dates, y=[c["avg_weighted_score"] or 0 for c in cycle_data], marker_color="#36A2EB"))
    cycle_fig.update_layout(title="Cycle-Level Averages", barmode="group", xaxis_title="Cycle End Date", yaxis_title="Value", xaxis_tickangle=-45)
    cycle_plot = plot(cycle_fig, output_type="div", config={"displayModeBar": False})

    # ---------------- 4. Metrics by Responsible Body + Cycle ----------------
    body_cycle_data = defaultdict(lambda: defaultdict(lambda: {"percent_achieved": [], "variance": [], "weighted_score": []}))
    for r in reports:
        date_label = r.action_plan.strategic_cycle.end_date.strftime("%B %Y") if r.action_plan.strategic_cycle and r.action_plan.strategic_cycle.end_date else "N/A"
        for body in r.action_plan.responsible_bodies.all():
            body_cycle_data[body.stakeholder_name][date_label]["percent_achieved"].append(r.percent_achieved or 0)
            body_cycle_data[body.stakeholder_name][date_label]["variance"].append(r.variance or 0)
            body_cycle_data[body.stakeholder_name][date_label]["weighted_score"].append(r.weighted_score or 0)

    all_dates = sorted({d for b in body_cycle_data.values() for d in b.keys()})
    body_fig = make_subplots(rows=3, cols=1, subplot_titles=("Avg % Achieved", "Avg Variance", "Avg Weighted Score"), vertical_spacing=0.15)
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, (body_name, date_data) in enumerate(body_cycle_data.items()):
        color = palette[i % len(palette)]
        body_fig.add_trace(go.Bar(name=body_name, x=all_dates, y=[(sum(date_data[d]["percent_achieved"]) / len(date_data[d]["percent_achieved"])) if date_data[d]["percent_achieved"] else 0 for d in all_dates], marker_color=color), row=1, col=1)
        body_fig.add_trace(go.Bar(name=body_name, x=all_dates, y=[(sum(date_data[d]["variance"]) / len(date_data[d]["variance"])) if date_data[d]["variance"] else 0 for d in all_dates], marker_color=color, showlegend=False), row=2, col=1)
        body_fig.add_trace(go.Bar(name=body_name, x=all_dates, y=[(sum(date_data[d]["weighted_score"]) / len(date_data[d]["weighted_score"])) if date_data[d]["weighted_score"] else 0 for d in all_dates], marker_color=color, showlegend=False), row=3, col=1)

    body_fig.update_layout(height=900, title="Performance by Responsible Body & Cycle", barmode="group", xaxis_tickangle=-45)
    body_plot = plot(body_fig, output_type="div", config={"displayModeBar": False})

    # ---------------- 5. KPI Trend Chart ----------------
    kpi_data = reports.values("action_plan__strategy_map__kpi", "action_plan__strategic_cycle__end_date", "achievement").order_by("action_plan__strategic_cycle__end_date")
    kpi_fig = go.Figure()
    for kpi in set([k["action_plan__strategy_map__kpi"] for k in kpi_data if k["action_plan__strategy_map__kpi"]]):
        x_vals, y_vals = [], []
        for d in kpi_data:
            if d["action_plan__strategy_map__kpi"] == kpi:
                x_vals.append(d["action_plan__strategic_cycle__end_date"].strftime("%B %Y") if d["action_plan__strategic_cycle__end_date"] else "N/A")
                y_vals.append(d["achievement"] or 0)
        kpi_fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines+markers", name=kpi))
    kpi_fig.update_layout(title="KPI Achievement Over Time", xaxis_title="Cycle End Date", yaxis_title="Achievement")
    kpi_plot = plot(kpi_fig, output_type="div", config={"displayModeBar": False})

    # ---------------- Context ----------------
    context = {
        "total_reports": total_reports,
        "avg_percent_achieved": avg_percent_achieved,
        "avg_variance": avg_variance,
        "avg_weighted_score": avg_weighted_score,
        "status_plot": status_plot,
        "cycle_plot": cycle_plot,
        "body_plot": body_plot,
        "kpi_plot": kpi_plot,
        "strategic_cycles": StrategicCycle.objects.all(),
        "responsible_bodies": sorted({b.stakeholder_name for r in StrategicReport.objects.all().prefetch_related("action_plan__responsible_bodies") for b in r.action_plan.responsible_bodies.all()}),
        "time_horizons": sorted({r.action_plan.strategic_cycle.time_horizon_type for r in StrategicReport.objects.all().select_related("action_plan__strategic_cycle") if r.action_plan.strategic_cycle and r.action_plan.strategic_cycle.time_horizon_type}),
        "selected_cycle": cycle_filter,
        "selected_body": body_filter,
        "selected_horizon": horizon_filter,
        "current_date": datetime.now(),
    }

    return render(request, "strategic_report/chart.html", context)









