from django.urls import path
from .views import DashboardHomeView,UserListView, UserDeleteView
# , DesignListView, DesignDeleteView, CommentListView, CommentDeleteView

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('users/', UserListView.as_view(), name='moderator-user-list'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='moderator-user-delete'),
    # path('designs/', DesignListView.as_view(), name='moderator-design-list'),
    # path('designs/<int:pk>/delete/', DesignDeleteView.as_view(), name='moderator-design-delete'),
    # path('comments/', CommentListView.as_view(), name='moderator-comment-list'),
    # path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='moderator-comment-delete'),
]
