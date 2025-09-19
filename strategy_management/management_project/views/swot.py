from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management_project.models import SwotAnalysis
from management_project.forms import SwotAnalysisForm
from django.db.models import Q

# -------------------- SWOT LIST --------------------
@login_required
def swot_list(request):
    query = request.GET.get("search", "").strip()

    swots = SwotAnalysis.objects.filter(
        organization_name=request.user.organization_name
    )

    if query:
        swots = swots.filter(
            Q(swot_type__icontains=query) |
            Q(swot_pillar__icontains=query)
        )

    swots = swots.order_by("swot_type", "priority", "-created_at")

    return render(request, "swot/list.html", {
        "swots": swots,
        "search_query": query,
    })


# -------------------- CREATE SWOT --------------------


@login_required
def create_swot(request):
    if request.method == 'POST':
        form = SwotAnalysisForm(request.POST)
        # Only save if the Save button is clicked
        if 'save' in request.POST and form.is_valid():
            swot_entry = form.save(commit=False)
            swot_entry.organization_name = request.user.organization_name
            swot_entry.save()
            messages.success(request, "SWOT entry created successfully!")
            return redirect('swot_list')
    else:
        form = SwotAnalysisForm()

    return render(request, 'swot/form.html', {'form': form})


# -------------------- UPDATE SWOT --------------------
@login_required
def update_swot(request, pk):
    # Fetch the entry only if it belongs to the user's organization
    entry = get_object_or_404(SwotAnalysis, pk=pk, organization_name=request.user.organization_name)

    if request.method == 'POST':
        form = SwotAnalysisForm(request.POST, instance=entry)
        if 'save' in request.POST and form.is_valid():
            form.save()
            messages.success(request, "SWOT entry updated successfully!")
            return redirect('swot_list')
        else:
            messages.error(request, "Error updating SWOT entry. Please check the form.")
    else:
        form = SwotAnalysisForm(instance=entry)

    return render(request, 'swot/form.html', {'form': form})


# -------------------- DELETE SWOT --------------------

@login_required
def delete_swot(request, pk):
    entry = get_object_or_404(
        SwotAnalysis,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        entry.delete()
        messages.success(request, "SWOT entry deleted successfully!")
        return redirect('swot_list')

    return render(request, 'swot/delete_confirm.html', {'entry': entry})