from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DeleteView
from django.urls import reverse_lazy
from account.models import CustomUser
from django.conf import settings

class DashboardHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def test_func(self):
        return self.request.user.is_moderator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Admin Dashboard'
        return context




# List all users
class UserListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'dashboard/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_moderator
    
    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['active_users'] = CustomUser.objects.filter(is_active=True).count()
        return context

    

# Delete a user
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'dashboard/user_confirm_delete.html'
    success_url = reverse_lazy('moderator-user-list')
    
    def test_func(self):
        return self.request.user.is_moderator   
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_staff=True)