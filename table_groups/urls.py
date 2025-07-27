from django.urls import path, include

from table_groups.views import MyTablesListView, CreateTableView, TableDetailView, ManageTableView

urlpatterns = [
    path('my_tables/', MyTablesListView.as_view(), name='my_tables'),
    path('create_table/', CreateTableView.as_view(), name='create_table'),
    path('<int:pk>/', include([
        path('table_details/', TableDetailView.as_view(), name='table_details'),
        path('manage_table/', ManageTableView.as_view(), name='manage_table'),
    ])),
]