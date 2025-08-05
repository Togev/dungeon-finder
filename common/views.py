from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from ads.models import Ad
from table_messages.models import TableMessage


def home(request):
    if request.user.is_authenticated:
        ads = Ad.objects.all().order_by('-created')
        q = request.GET.get('q')
        if q:
            ads = ads.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(owner__username__icontains=q)
            )
        paginator = Paginator(ads, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'ads/ad_list.html', {'page_obj': page_obj})
    else:
        ads_created = Ad.objects.count()
        active_members = get_user_model().objects.filter(is_active=True).count()
        messages_sent = TableMessage.objects.count()
        return render(request, 'common/landing.html', {
            'ads_created': ads_created,
            'active_members': active_members,
            'messages_sent': messages_sent,
        })