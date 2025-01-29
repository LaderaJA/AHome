from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from .models import Design, Like, Comment, Follow, CapturedImage
from account.models import CustomUser
from django.utils.timezone import now
from .forms import CommentForm
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designs'] = Design.objects.all()[:10]  
        return context

class DesignListView(ListView):
    model = Design
    template_name = "pages/design_list.html"
    context_object_name = "designs"
    ordering = "-created_at"

    def get_queryset(self):
        queryset = Design.objects.all()
        query = self.request.GET.get('q')
        sort_option = self.request.GET.get("sort", "")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(creator__username__icontains=query)
            )

        if sort_option in ["title", "-created_at", "created_at"]:  # Ensure valid sort options
            queryset = queryset.order_by(sort_option)

        return queryset

class DesignDetailView(DetailView):
    model = Design
    template_name = 'pages/design_detail.html'
    context_object_name = 'design'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        design = self.get_object()
        user = self.request.user
        
        if user.is_authenticated:
            context['can_edit_or_delete'] = (
                user == design.creator or user.is_staff or (user.is_moderator == True)
            )
            context['has_liked'] = design.likes.filter(user=user).exists()
        else:
            context['can_edit_or_delete'] = False
            context['has_liked'] = False
            
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object =  self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.design = self.object
            comment.save()
            return redirect(reverse('design-detail', kwargs={'pk': self.object.pk}))
        return self.get(self, request, *args, **kwargs)

class DesignCreateView(LoginRequiredMixin, CreateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    success_url = reverse_lazy('design-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class DesignUpdateView(LoginRequiredMixin, UpdateView):
    model = Design
    fields = ['title', 'description', 'image']
    template_name = 'pages/design_form.html'
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.pk}) 

class DesignDeleteView(LoginRequiredMixin, DeleteView):
    model = Design
    template_name = 'pages/design_confirm_delete.html'
    success_url = reverse_lazy('design-list')  

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = "pages/comment_form.html"

    def get_queryset(self):
        if self.request.user.is_moderator:
            return Comment.objects.all()
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.design.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "pages/confirm_comment_delete.html"

    def get_queryset(self):
        if self.request.user.is_moderator:
            return Comment.objects.all()
        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('design-detail', kwargs={'pk': self.object.design.pk})

# like functions
class LikeDesignView(View):
    def post(self, request, pk):
        design = get_object_or_404(Design, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, design=design)

        if not created:
            like.delete()
        
        return redirect('design-detail', pk=pk)

# follow functions
class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        User = get_user_model()
        user_to_follow = get_object_or_404(User, pk=pk)

        if request.user != user_to_follow:
            follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
            
            if not created:  
                follow.delete()

        return redirect('profile', pk=user_to_follow.pk )

class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        User = get_user_model()
        user_to_unfollow = get_object_or_404(User, pk=pk)

        if request.user != user_to_unfollow:
            follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow).first()
            
            if follow:
                follow.delete()

        return redirect('profile', pk=user_to_unfollow.pk)



# camera
class CameraFilterView(TemplateView):
    template_name = "pages/camera_filter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['designs'] = Design.objects.all()  
        return context

class SaveCapturedImageView(CreateView):
    model = CapturedImage
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        image_data = request.POST.get("image")
        if image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f"captured.{ext}")

            captured_image = CapturedImage.objects.create(user=request.user, image=image)
            return JsonResponse({"message": "Image saved successfully!", "image_url": captured_image.image.url}, status=200)
        
        return JsonResponse({"error": "Invalid image data"}, status=400)
    
    #gallery
class CapturedImageGalleryView(LoginRequiredMixin, ListView):
    model = CapturedImage
    template_name = 'pages/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        return CapturedImage.objects.filter(user=self.request.user)
    
class CapturedImageDeleteView(LoginRequiredMixin, DeleteView):
    model = CapturedImage
    template_name = 'pages/confirm_delete_image.html'
    context_object_name = 'image'
    success_url = reverse_lazy('gallery')

    def get_queryset(self):
        return CapturedImage.objects.filter(user=self.request.user)