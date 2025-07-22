from django.contrib.auth.views import LogoutView
from django.urls import path, include

from accounts import views
from accounts.views import UserDetailView

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('<int:pk>/', include([
        path('details/', UserDetailView.as_view(), name='account_details'),
        path('edit/', views.EditProfileView.as_view(), name='account_edit'),
        path('delete/', views.DeleteAccountView.as_view(), name='account_delete'),
    ])),
]