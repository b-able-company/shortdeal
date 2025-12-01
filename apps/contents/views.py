"""
Template-based views for content browsing
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Content
from apps.booths.models import Booth
from apps.core.constants import CONTENT_STATUS_PUBLIC


def browse_view(request):
    """
    콘텐츠 브라우징 화면 (/browse)
    - BRW-001~006: 카드 리스트, 검색, 필터, 페이지네이션
    - 권한: AllowAny (전체 공개)
    """
    # Get all public contents
    contents = Content.objects.filter(status=CONTENT_STATUS_PUBLIC).select_related('producer')

    # Search (BRW-002)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        contents = contents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(producer__company_name__icontains=search_query)
        )

    # Genre filter (BRW-003)
    genre_filter = request.GET.getlist('genre')
    if genre_filter:
        for genre in genre_filter:
            contents = contents.filter(genre_tags__contains=[genre])

    # Price range filter (BRW-004)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if price_min:
        try:
            contents = contents.filter(price__gte=float(price_min))
        except ValueError:
            pass

    if price_max:
        try:
            contents = contents.filter(price__lte=float(price_max))
        except ValueError:
            pass

    # Sorting
    ordering = request.GET.get('ordering', '-created_at')
    if ordering in ['-created_at', 'created_at', 'price', '-price']:
        contents = contents.order_by(ordering)

    # Pagination (BRW-005: 20개 단위)
    paginator = Paginator(contents, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Genre choices for filter
    genre_choices = [
        'drama', 'comedy', 'romance', 'action', 'thriller',
        'horror', 'documentary', 'education', 'business',
        'lifestyle', 'food', 'travel', 'music', 'sports', 'gaming'
    ]

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'price_min': price_min,
        'price_max': price_max,
        'ordering': ordering,
        'genre_choices': genre_choices,
        'total_count': paginator.count,
    }

    return render(request, 'contents/browse.html', context)


def content_detail_view(request, content_id):
    """
    콘텐츠 상세 화면 (/content/:contentId)
    - CNT-001~004: 기본 정보, 제작사 정보, 링크, 오퍼 버튼
    - 권한: AllowAny (전체 공개)
    """
    content = get_object_or_404(
        Content.objects.select_related('producer'),
        pk=content_id,
        status=CONTENT_STATUS_PUBLIC
    )

    # Increment view count (CNT-001)
    content.increment_view_count()

    # Check if user can submit offer (CNT-004)
    can_submit_offer = False
    if request.user.is_authenticated and request.user.role == 'buyer':
        can_submit_offer = True

    context = {
        'content': content,
        'can_submit_offer': can_submit_offer,
    }

    return render(request, 'contents/detail.html', context)


def booth_view(request, slug):
    """
    제작사 부스 화면 (/booth/:slug)
    - BTH-001~002: 제작사 정보, 콘텐츠 리스트
    - 권한: AllowAny (전체 공개)
    """
    booth = get_object_or_404(Booth.objects.select_related('producer'), slug=slug)

    # Get producer's public contents (BTH-002)
    contents = Content.objects.filter(
        producer=booth.producer,
        status=CONTENT_STATUS_PUBLIC
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(contents, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'booth': booth,
        'producer': booth.producer,
        'page_obj': page_obj,
        'total_count': paginator.count,
    }

    return render(request, 'booths/detail.html', context)
