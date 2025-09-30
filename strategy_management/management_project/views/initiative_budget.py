from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from management_project.models import InitiativeBudget, Initiative
from management_project.forms import InitiativeBudgetForm

# -------------------- LIST BUDGETS --------------------
@login_required
def initiative_budget_list(request):
    query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    # All budgets for initiatives in the user's organization
    budgets = InitiativeBudget.objects.filter(
        organization_name=request.user.organization_name
    ).select_related('initiative')

    # Search filter across initiative fields
    if query:
        budgets = budgets.filter(
            Q(initiative__initiative_name__icontains=query) |
            Q(initiative__initiative_dimension__icontains=query) |
            Q(initiative__initiative_focus_area__icontains=query)
        )

    # Ordering by initiative name
    budgets = budgets.order_by('initiative__initiative_name')

    # Pagination
    paginator = Paginator(budgets, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'initiative_budget/list.html', {
        'budgets': page_obj,
        'page_obj': page_obj,
        'search_query': query,
    })


# -------------------- CREATE BUDGET --------------------
@login_required
def create_initiative_budget(request):
    if request.method == 'POST':
        form = InitiativeBudgetForm(request.POST, request=request)
        if 'save' in request.POST and form.is_valid():
            budget = form.save(commit=False)
            budget.organization_name = request.user.organization_name
            budget.save()
            messages.success(request, "Initiative budget created successfully!")
            return redirect('initiative_budget_list')
    else:
        form = InitiativeBudgetForm(request=request)

    return render(request, 'initiative_budget/form.html', {'form': form})


# -------------------- UPDATE BUDGET --------------------
@login_required
def update_initiative_budget(request, pk):
    budget = get_object_or_404(
        InitiativeBudget,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = InitiativeBudgetForm(request.POST, instance=budget, request=request)
        if 'save' in request.POST and form.is_valid():
            form.save()
            messages.success(request, "Initiative budget updated successfully!")
            return redirect('initiative_budget_list')
        else:
            messages.error(request, "Error updating budget. Please check the form.")
    else:
        form = InitiativeBudgetForm(instance=budget, request=request)

    return render(request, 'initiative_budget/form.html', {'form': form})


# -------------------- DELETE BUDGET --------------------
@login_required
def delete_initiative_budget(request, pk):
    budget = get_object_or_404(
        InitiativeBudget,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Initiative budget deleted successfully!")
        return redirect('initiative_budget_list')

    return render(request, 'initiative_budget/delete_confirm.html', {'budget': budget})
