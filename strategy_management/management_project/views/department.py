from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management_project.models import Department
from management_project.forms import DepartmentForm

# -------------------- DEPARTMENT LIST --------------------
@login_required
def department_list(request):
    departments = Department.objects.filter(
        organization_name=request.user.organization_name
    ).order_by('department_name')

    form = DepartmentForm()

    context = {
        'departments': departments,
        'form': form,
    }
    return render(request, 'department/list.html', context)


# -------------------- CREATE DEPARTMENT --------------------
@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.organization_name = request.user.organization_name
            department.save()
            messages.success(request, "Department created successfully!")
            return redirect('department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm()

    departments = Department.objects.filter(
        organization_name=request.user.organization_name
    ).order_by('department_name')

    return render(request, 'department/list.html', {'form': form, 'departments': departments})


# -------------------- UPDATE DEPARTMENT --------------------
@login_required
def update_department(request, pk):
    department = get_object_or_404(
        Department,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm(instance=department)

    departments = Department.objects.filter(
        organization_name=request.user.organization_name
    ).order_by('department_name')

    context = {
        'form': form,
        'edit_mode': True,
        'editing_department': department,
        'departments': departments,
    }
    return render(request, 'department/list.html', context)


# -------------------- DELETE DEPARTMENT --------------------
@login_required
def delete_department(request, pk):
    department = get_object_or_404(
        Department,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')

    return render(request, 'department/delete_confirm.html', {'department': department})
