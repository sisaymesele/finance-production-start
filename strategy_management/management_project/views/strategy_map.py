from django.shortcuts import render, redirect, get_object_or_404
from management_project.models import StrategyMap
from management_project.forms import StrategyMapForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def strategy_map_list(request):
    """
    List all strategy map entries belonging to the current user's organization,
    with optional search on perspective, pillar, and objective.
    """
    # Base queryset filtered by user's organization
    strategies = StrategyMap.objects.filter(
        organization_name=request.user.organization_name
    )

    # Get search query
    query = request.GET.get('q', '')
    if query:
        strategies = strategies.filter(
            Q(strategic_perspective__icontains=query) |
            Q(strategic_pillar__icontains=query) |
            Q(objective__icontains=query)
        )

    return render(request, 'strategy_map/list.html', {
        'strategies': strategies,
        'query': query,  # pass back search term to template
    })


@login_required
def create_strategy_map(request):
    """
    Create a new strategy map entry for the current user's organization.
    """
    if request.method == 'POST':
        form = StrategyMapForm(request.POST)
        if 'save' in request.POST and form.is_valid():
            strategy = form.save(commit=False)
            strategy.organization_name = request.user.organization_name
            strategy.save()
            return redirect('strategy_map_list')
    else:
        form = StrategyMapForm()

    return render(request, 'strategy_map/form.html', {'form': form})


@login_required
def update_strategy_map(request, pk):
    """
    Update an existing strategy map entry, only if it belongs to the user's organization.
    """
    entry = get_object_or_404(
        StrategyMap,
        pk=pk,
        organization_name=request.user.organization_name
    )
    if request.method == 'POST':
        form = StrategyMapForm(request.POST, instance=entry)
        if 'save' in request.POST and form.is_valid():
            form.save()
            return redirect('strategy_map_list')
    else:
        form = StrategyMapForm(instance=entry)

    return render(request, 'strategy_map/form.html', {'form': form})


@login_required
def delete_strategy_map(request, pk):
    """
    Delete an existing strategy map entry, only if it belongs to the user's organization.
    """
    entry = get_object_or_404(
        StrategyMap,
        pk=pk,
        organization_name=request.user.organization_name
    )
    if request.method == 'POST':
        entry.delete()
        return redirect('strategy_map_list')

    return render(request, 'strategy_map/delete_confirm.html', {'entry': entry})
