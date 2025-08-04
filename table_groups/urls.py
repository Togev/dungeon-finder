from django.urls import path, include

from table_groups.views import MyTablesListView, CreateTableView, TableDetailView, ManageTableView, \
    TableDemoteAdminView, TablePromoteAdminView, TableRemoveMemberView, TableTransferOwnershipView, TableDeleteView, \
    TableLeaveView, AjaxTableMessagesView

urlpatterns = [
    path('my_tables/', MyTablesListView.as_view(), name='my_tables'),
    path('create_table/', CreateTableView.as_view(), name='create_table'),
    path('<int:pk>/', include([
        path('table_details/', TableDetailView.as_view(), name='table_details'),
        path('messages/ajax/', AjaxTableMessagesView.as_view(), name='ajax_table_messages'),
        path('manage_table/', ManageTableView.as_view(), name='manage_table'),
        path('demote_admin/<int:member_id>/', TableDemoteAdminView.as_view(), name='table_demote_admin'),
        path('promote_admin/<int:member_id>/', TablePromoteAdminView.as_view(), name='table_promote_admin'),
        path('remove_member/<int:member_id>/', TableRemoveMemberView.as_view(), name='table_remove_member'),
        path('transfer_ownership/<int:member_id>/', TableTransferOwnershipView.as_view(), name='table_transfer_ownership'),
        path('delete/', TableDeleteView.as_view(), name='table_delete'),
        path('leave/', TableLeaveView.as_view(), name='table_leave'),
    ])),
]