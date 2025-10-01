from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from management_project.models import InitiativeResource, Initiative
from management_project.forms import InitiativeResourceForm

# # -------------------- LIST RESOURCES --------------------
# -------------------- LIST RESOURCES --------------------
@login_required
def initiative_resource_list(request):
    query = request.GET.get('search', '').strip()
    selected_initiative = request.GET.get('initiative', '').strip()
    page_number = request.GET.get('page', 1)

    # Base queryset: all resources for initiatives in the user's organization
    resources = InitiativeResource.objects.filter(
        organization_name=request.user.organization_name
    ).select_related('initiative')

    # Initiative filter
    selected_initiative_name = None
    if selected_initiative:
        resources = resources.filter(initiative_id=selected_initiative)
        initiative_obj = Initiative.objects.filter(pk=selected_initiative).first()
        if initiative_obj:
            selected_initiative_name = initiative_obj.initiative_name

    # Search filter across initiative fields + resource_type
    if query:
        resources = resources.filter(
            Q(initiative__initiative_name__icontains=query) |
            Q(initiative__initiative_dimension__icontains=query) |
            Q(initiative__initiative_focus_area__icontains=query) |
            Q(resource_type__icontains=query)
        )

    # Ordering
    resources = resources.order_by('initiative__initiative_name', 'resource_type')

    # Pagination
    paginator = Paginator(resources, 10)
    page_obj = paginator.get_page(page_number)

    # Initiatives for dropdown
    initiatives = Initiative.objects.filter(
        organization_name=request.user.organization_name
    ).order_by('initiative_name')

    return render(request, 'initiative_resource/list.html', {
        'resources': page_obj,
        'page_obj': page_obj,
        'search_query': query,
        'initiatives': initiatives,
        'selected_initiative': selected_initiative,
        'selected_initiative_name': selected_initiative_name,
    })


# -------------------- CREATE RESOURCE --------------------
# @login_required
# def create_initiative_resource(request):
#     if request.method == 'POST':
#         form = InitiativeResourceForm(request.POST, request=request)
#         if 'save' in request.POST and form.is_valid():
#             resource = form.save(commit=False)
#             resource.organization_name = request.user.organization_name
#             resource.save()
#             messages.success(request, "Initiative resource created successfully!")
#             return redirect('initiative_resource_list')
#     else:
#         form = InitiativeResourceForm(request=request)
#
#     return render(request, 'initiative_resource/form.html', {'form': form})

@login_required
def create_initiative_resource(request):
    selected_initiative = request.GET.get('initiative')  # Preselect if passed
    if request.method == 'POST':
        form = InitiativeResourceForm(request.POST, request=request)
        if form.is_valid() and 'save' in request.POST:
            resource = form.save(commit=False)
            resource.organization_name = request.user.organization_name
            resource.save()
            messages.success(request, "Initiative resource created successfully!")
            return redirect('initiative_resource_list')  # or stay on child list
    else:
        initial_data = {}
        if selected_initiative:
            initial_data['initiative'] = selected_initiative
        form = InitiativeResourceForm(initial=initial_data, request=request)

    return render(request, 'initiative_resource/form.html', {
        'form': form,
        'next': None  # child form doesn't need next
    })

# -------------------- UPDATE RESOURCE --------------------
@login_required
def update_initiative_resource(request, pk):
    resource = get_object_or_404(
        InitiativeResource,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = InitiativeResourceForm(request.POST, instance=resource, request=request)
        if 'save' in request.POST and form.is_valid():
            form.save()
            messages.success(request, "Initiative resource updated successfully!")
            return redirect('initiative_resource_list')
        else:
            messages.error(request, "Error updating resource. Please check the form.")
    else:
        form = InitiativeResourceForm(instance=resource, request=request)

    return render(request, 'initiative_resource/form.html', {'form': form})


# -------------------- DELETE RESOURCE --------------------
@login_required
def delete_initiative_resource(request, pk):
    resource = get_object_or_404(
        InitiativeResource,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Initiative resource deleted successfully!")
        return redirect('initiative_resource_list')

    return render(request, 'initiative_resource/delete_confirm.html', {'resource': resource})
