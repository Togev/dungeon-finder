from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from ads.models import Ad

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
        # return the context as you do now, e.g.
        return render(request, 'ads/ad_list.html', {'page_obj': page_obj})
    else:
        recent_ads = Ad.objects.all().order_by('-created')[:3]
        return render(request, 'common/landing.html', {
            'recent_ads': recent_ads,
            'blurb': "Welcome to RPG Ad Board! Post or find campaigns to join.",
            'show_full_list': False,
        })