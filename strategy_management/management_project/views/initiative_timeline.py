from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from management_project.models import InitiativeTimeline, Initiative
from management_project.forms import InitiativeTimelineForm

# -------------------- LIST TIMELINES --------------------
# -------------------- LIST TIMELINES --------------------
@login_required
def initiative_timeline_list(request):
    query = request.GET.get('search', '').strip()
    selected_initiative = request.GET.get('initiative', '').strip()
    page_number = request.GET.get('page', 1)

    # Base queryset: all timelines for initiatives in the user's organization
    timelines = InitiativeTimeline.objects.filter(
        organization_name=request.user.organization_name
    ).select_related('initiative')

    # Initiative filter
    selected_initiative_name = None
    if selected_initiative:
        timelines = timelines.filter(initiative_id=selected_initiative)
        initiative_obj = Initiative.objects.filter(pk=selected_initiative).first()
        if initiative_obj:
            selected_initiative_name = initiative_obj.initiative_name

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

    # Pass initiatives for dropdown filter
    initiatives = Initiative.objects.filter(
        organization_name=request.user.organization_name
    ).order_by('initiative_name')

    return render(request, 'initiative_timeline/list.html', {
        'timelines': page_obj,
        'page_obj': page_obj,
        'search_query': query,
        'initiatives': initiatives,
        'selected_initiative': selected_initiative,
        'selected_initiative_name': selected_initiative_name,
    })


# -------------------- CREATE TIMELINE --------------------
# @login_required
# def create_initiative_timeline(request):
#     if request.method == 'POST':
#         form = InitiativeTimelineForm(request.POST, request=request)
#         if 'save' in request.POST and form.is_valid():
#             timeline = form.save(commit=False)
#             timeline.organization_name = request.user.organization_name
#             timeline.save()
#             messages.success(request, "Initiative timeline created successfully!")
#             return redirect('initiative_timeline_list')
#     else:
#         form = InitiativeTimelineForm(request=request)
#
#     return render(request, 'initiative_timeline/form.html', {'form': form})

@login_required
def create_initiative_timeline(request):
    selected_initiative = request.GET.get('initiative')  # Preselect if passed
    if request.method == 'POST':
        form = InitiativeTimelineForm(request.POST, request=request)
        if form.is_valid() and 'save' in request.POST:
            timeline = form.save(commit=False)
            timeline.organization_name = request.user.organization_name
            timeline.save()
            messages.success(request, "Initiative timeline created successfully!")
            return redirect('initiative_timeline_list')  # or keep in child list page
    else:
        initial_data = {}
        if selected_initiative:
            initial_data['initiative'] = selected_initiative
        form = InitiativeTimelineForm(initial=initial_data, request=request)

    return render(request, 'initiative_timeline/form.html', {
        'form': form,
        'next': None  # child form doesn't need next
    })


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
