from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management_project.models import Vision
from management_project.forms import VisionForm
from django.core.paginator import Paginator

# -------------------- VISION LIST --------------------
@login_required
def vision_list(request):
    """
    List all visions for the logged-in user's organization.
    Superusers see all visions.
    """
    if request.user.is_superuser:
        visions = Vision.objects.all().order_by('-id')
    else:
        visions = Vision.objects.filter(organization_name=request.user.organization_name)

    paginator = Paginator(visions, 10)  # 10 visions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = VisionForm()  # Empty form for creating new visions

    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'vision/list.html', context)


# -------------------- CREATE VISION --------------------
@login_required
def create_vision(request):
    if request.method == 'POST':
        form = VisionForm(request.POST)
        if form.is_valid():
            vision = form.save(commit=False)
            vision.organization_name = request.user.organization_name
            vision.save()
            messages.success(request, "Vision created successfully!")
            return redirect('vision_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VisionForm()

    return render(request, 'vision/list.html', {'form': form})


# -------------------- UPDATE VISION --------------------
@login_required
def update_vision(request, pk):
    vision = get_object_or_404(
        Vision,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        form = VisionForm(request.POST, instance=vision)
        if form.is_valid():
            form.save()
            messages.success(request, "Vision updated successfully!")
            return redirect('vision_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VisionForm(instance=vision)

    context = {
        'form': form,
        'edit_mode': True,
        'editing_vision': vision,
    }
    return render(request, 'vision/list.html', context)


# -------------------- DELETE VISION --------------------
@login_required
def delete_vision(request, pk):
    vision = get_object_or_404(
        Vision,
        pk=pk,
        organization_name=request.user.organization_name
    )

    if request.method == 'POST':
        vision.delete()
        messages.success(request, "Vision deleted successfully!")
        return redirect('vision_list')  # after deletion, redirect to main list

    # GET → show confirmation page
    return render(request, 'vision/delete_confirm.html', {'vision': vision})



