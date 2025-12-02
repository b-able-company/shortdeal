"""
LOI views for buyers and producers
"""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q

from .models import LOI


@login_required
def loi_list_view(request):
    """
    View list of LOIs for current user (both as buyer and producer)
    Screen 16: /loi
    """
    # Get all LOIs where user is either buyer or producer
    lois = LOI.objects.filter(
        Q(buyer=request.user) | Q(producer=request.user)
    ).select_related('offer', 'buyer', 'producer').order_by('-created_at')

    # Role filter
    role_filter = request.GET.get('role', '')
    if role_filter == 'buyer':
        lois = lois.filter(buyer=request.user)
    elif role_filter == 'producer':
        lois = lois.filter(producer=request.user)

    # Summary stats
    summary = {
        'total': lois.count(),
        'as_buyer': LOI.objects.filter(buyer=request.user).count(),
        'as_producer': LOI.objects.filter(producer=request.user).count(),
    }

    # Pagination
    paginator = Paginator(lois, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'loi/list.html', {
        'page_obj': page_obj,
        'summary': summary,
        'role_filter': role_filter,
    })


@login_required
def loi_detail_view(request, loi_id):
    """
    View LOI details
    Screen 17: /loi/:loiId
    """
    # Get LOI
    loi = get_object_or_404(LOI, id=loi_id)

    # Check permission: user must be either buyer or producer
    if request.user != loi.buyer and request.user != loi.producer:
        raise Http404("LOI not found")

    # Determine user's role in this LOI
    user_role = 'buyer' if request.user == loi.buyer else 'producer'

    return render(request, 'loi/detail.html', {
        'loi': loi,
        'user_role': user_role,
    })
