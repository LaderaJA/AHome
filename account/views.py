from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import CustomUser
from AHome_app.models import Follow, Design
from django.contrib.auth import logout

class RegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your account has been created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating your account. Please check the details and try again.")
        return super().form_invalid(form)



class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/profile.html' 
    context_object_name = 'user' 

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        context['user_designs'] = Design.objects.filter(creator=profile_user)
        context['followers_count'] = Follow.objects.filter(followed=profile_user).count()
        context['following_count'] = Follow.objects.filter(follower=profile_user).count()
        context['is_following'] = Follow.objects.filter(follower=self.request.user, followed=profile_user).exists()    
        return context

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'account/profile_confirm_delete.html'  
    def get_success_url(self):
        logout(self.request)
    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/profile_edit.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user  

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        is_following = Follow.objects.filter(follower=self.request.user, followed=profile_user).exists()
        context['is_following'] = is_following
        return context
    