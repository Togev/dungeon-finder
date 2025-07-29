from django.urls import path
from table_messages.views import TableMessageDeleteView

urlpatterns = [
    path('<int:pk>/delete/', TableMessageDeleteView.as_view(), name='delete_message'),
]