from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from management_project.models import InitiativeTimeline, Initiative
from management_project.forms import InitiativeTimelineForm

# -------------------- LIST TIMELINES --------------------
@login_required
def initiative_timeline_list(request):
    query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    # All timelines for initiatives in the user's organization
    timelines = InitiativeTimeline.objects.filter(
        organization_name=request.user.organization_name
    ).select_related('initiative')

    # Search filter across initiative fields
    if query:
        timelines = timelines.filter(
            Q(initiative__initiative_name__icontains=query) |
            Q(initiative__initiative_dimension__icontains=query) |
            Q(initiative__initiative_focus_area__icontains=query)
        )

    # Ordering by start_date descending
    timelines = timelines.order_by('-start_date', 'initiative__initiative_name')

    # Pagination
    paginator = Paginator(timelines, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'initiative_timeline/list.html', {
        'timelines': page_obj,
        'page_obj': page_obj,
        'search_query': query,
    })


# -------------------- CREATE TIMELINE --------------------
@login_required
def create_initiative_timeline(request):
    if request.method == 'POST':
        form = InitiativeTimelineForm(request.POST, request=request)
        if 'save' in request.POST and form.is_valid():
            timeline = form.save(commit=False)
            timeline.organization_name = request.user.organization_name
            timeline.save()
            messages.success(request, "Initiative timeline created successfully!")
            return redirect('initiative_timeline_list')
    else:
        form = InitiativeTimelineForm(request=request)

    return render(request, 'initiative_timeline/form.html', {'form': form})


# -------------------- UPDATE TIMELINE --------------------
@login_required
def update_initiative_timeline(request, pk):
    timeline = get_object_or_404(
        InitiativeTimeline,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = InitiativeTimelineForm(request.POST, instance=timeline, request=request)
        if 'save' in request.POST and form.is_valid():
            form.save()
            messages.success(request, "Initiative timeline updated successfully!")
            return redirect('initiative_timeline_list')
        else:
            messages.error(request, "Error updating timeline. Please check the form.")
    else:
        form = InitiativeTimelineForm(instance=timeline, request=request)

    return render(request, 'initiative_timeline/form.html', {'form': form})


# -------------------- DELETE TIMELINE --------------------
@login_required
def delete_initiative_timeline(request, pk):
    timeline = get_object_or_404(
        InitiativeTimeline,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        timeline.delete()
        messages.success(request, "Initiative timeline deleted successfully!")
        return redirect('initiative_timeline_list')

    return render(request, 'initiative_timeline/delete_confirm.html', {'timeline': timeline})
