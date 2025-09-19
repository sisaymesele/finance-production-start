from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Q, Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime

from management_project.models import Stakeholder, OrganizationalProfile
from management_project.forms import StakeholderForm

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import plotly.graph_objs as go
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment


@login_required
def stakeholder_list(request):
    """List stakeholders for the logged-in user's organization"""
    qs = Stakeholder.objects.filter(organization_name=request.user.organization_name)

    search_query = request.GET.get('search', '')
    if search_query:
        qs = qs.filter(
            Q(stakeholder_name__icontains=search_query) |
            Q(stakeholder_type__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(department__icontains=search_query)
        )

    # Order by priority descending
    qs = qs.order_by('-priority', 'stakeholder_name')

    # Pagination
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Count by role for quick summary
    count_by_role = qs.values('role').annotate(role_count=Count('role'))
    total_stakeholders = qs.count()

    context = {
        'page_obj': page_obj,
        'count_by_role': count_by_role,
        'total_stakeholders': total_stakeholders,
    }
    return render(request, 'stakeholder_list/list.html', context)


@login_required
def create_stakeholder(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = StakeholderForm(request.POST)
        if form.is_valid():
            stakeholder = form.save(commit=False)
            stakeholder.organization_name = request.user.organization_name
            stakeholder.save()
            messages.success(request, "Stakeholder created successfully!")
            return redirect(next_url or 'stakeholder_list')
    else:
        form = StakeholderForm()

    context = {
        'form': form,
        'form_title': 'Create Stakeholder',
        'submit_button_text': 'Create Stakeholder',
        'back_url': next_url or reverse('stakeholder_list'),
    }
    return render(request, 'stakeholder_list/form.html', context)


@login_required
def update_stakeholder(request, pk):
    stakeholder = get_object_or_404(Stakeholder, pk=pk, organization_name=request.user.organization_name)

    if request.method == 'POST':
        form = StakeholderForm(request.POST, instance=stakeholder)
        if form.is_valid():
            form.save()
            messages.success(request, "Stakeholder updated successfully!")
            return redirect('stakeholder_list')
    else:
        form = StakeholderForm(instance=stakeholder)

    context = {
        'form': form,
        'form_title': 'Update Stakeholder',
        'submit_button_text': 'Update Stakeholder',
        'back_url': request.GET.get('next', reverse('stakeholder_list')),
        'edit_mode': True,
        'editing_stakeholder': stakeholder,
    }
    return render(request, 'stakeholder_list/form.html', context)


@login_required
def delete_stakeholder(request, pk):
    stakeholder = get_object_or_404(Stakeholder, pk=pk, organization_name=request.user.organization_name)

    if request.method == 'POST':
        stakeholder.delete()
        messages.success(request, "Stakeholder deleted successfully!")
        return redirect('stakeholder_list')

    return render(request, 'stakeholder_list/delete_confirm.html', {'stakeholder': stakeholder})



@login_required
def export_stakeholders_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stakeholders"

    excluded_fields = {'slug', 'depends_on'}
    field_names = [
        field.name for field in Stakeholder._meta.get_fields()
        if not field.is_relation and field.name not in excluded_fields
    ]

    headers = [field.replace('_', ' ').title() for field in field_names]

    # 🔹 Title Row (Merged across all columns)
    title = f"Stakeholder List"
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    title_cell = ws.cell(row=1, column=1, value=title)
    title_cell.font = Font(size=14, bold=True, color="FFFFFFFF")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    title_cell.fill = PatternFill(start_color="FF305496", end_color="FF305496", fill_type="solid")

    # 🔹 Header Row
    ws.append(headers)
    header_row_idx = 2
    header_fill = PatternFill(start_color="FF0070C0", end_color="FF0070C0", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for cell in ws[header_row_idx]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment

    # 🔹 Fetch stakeholders
    stakeholders = Stakeholder.objects.filter(
        organization_name=request.user.organization_name
    ).values_list(*field_names)

    for s in stakeholders:
        row = []
        for value in s:
            if isinstance(value, datetime):
                row.append(value.date())
            else:
                row.append(value)
        ws.append(row)

    # 🔹 Auto column width
    for i, column_cells in enumerate(ws.columns, 1):
        max_length = max((len(str(cell.value)) for cell in column_cells if cell.value), default=0) + 2
        ws.column_dimensions[get_column_letter(i)].width = max(max_length, 12)

    # 🔹 Adjust row heights (title + header)
    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 20

    # 🔹 Response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename=stakeholders.xlsx'
    wb.save(response)
    return response



@login_required
def stakeholder_graph_view(request):
    qs = Stakeholder.objects.filter(organization_name=request.user.organization_name)

    # Example graphs: by role, by department, by stakeholder type
    role_counts = qs.values('role').annotate(count=Count('role'))
    dept_counts = qs.values('department').annotate(count=Count('department'))
    type_counts = qs.values('stakeholder_type').annotate(count=Count('stakeholder_type'))

    color_palette = ["ForestGreen", "RoyalBlue", "Magenta", "Orange", "Cyan", "Gold", "Crimson"]

    # Role bar chart
    role_labels = [r['role'] for r in role_counts]
    role_values = [r['count'] for r in role_counts]
    fig_role = go.Figure(data=[go.Bar(x=role_labels, y=role_values, marker=dict(color=color_palette[:len(role_labels)]))])
    fig_role.update_layout(title='Stakeholders by Role', xaxis_title='Role', yaxis_title='Count', template='plotly_white')

    # Department bar chart
    dept_labels = [d['department'] if d['department'] else 'Unknown' for d in dept_counts]
    dept_values = [d['count'] for d in dept_counts]
    fig_dept = go.Figure(data=[go.Bar(x=dept_labels, y=dept_values, marker=dict(color=color_palette[:len(dept_labels)]))])
    fig_dept.update_layout(title='Stakeholders by Department', xaxis_title='Department', yaxis_title='Count', template='plotly_white')

    # Stakeholder type pie chart
    type_labels = [t['stakeholder_type'] for t in type_counts]
    type_values = [t['count'] for t in type_counts]
    fig_type = go.Figure(data=[go.Pie(labels=type_labels, values=type_values, hole=0.3, marker=dict(colors=color_palette[:len(type_labels)]))])
    fig_type.update_layout(title='Stakeholders by Type')

    return render(request, 'stakeholder_list/graph.html', {
        'plot_html_role': fig_role.to_html(full_html=False),
        'plot_html_department': fig_dept.to_html(full_html=False),
        'plot_html_type': fig_type.to_html(full_html=False),
    })
