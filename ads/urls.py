from django.urls import path, include

from ads import views


urlpatterns = [
    path('create/', views.CreateAdView.as_view(), name='ad_create'),
    path('my_ads/', views.MyAdsListView.as_view(), name='my_ads'),
    path('<int:pk>/', include([
        path('details/', views.AdDetailView.as_view(), name='ad_details'),
        path('edit/', views.EditAdView.as_view(), name='ad_edit'),
        path('delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    ]))
]