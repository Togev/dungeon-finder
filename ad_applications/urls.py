from django.urls import path, include
import ad_applications.views
urlpatterns = [
    path('my_applications/', ad_applications.views.MyApplicationsListView.as_view(), name='my_applications'),
    path('application_form/<int:ad_id>/', ad_applications.views.ApplicationCreateView.as_view(), name='application_form'),
    path('<int:pk>/application_details/', ad_applications.views.ApplicationDetailView.as_view(), name='application_details'),
    path('<int:pk>/application_delete/', ad_applications.views.ApplicationDeleteView.as_view(), name='application_delete'),
    path('<int:pk>/application_accept/', ad_applications.views.ApplicationAcceptView.as_view(), name='application_accept'),
    path('<int:pk>/application_reject/', ad_applications.views.ApplicationRejectView.as_view(), name='application_reject'),
]