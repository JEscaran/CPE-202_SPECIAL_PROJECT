from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import HttpResponseForbidden
import random


def LoginPage(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('HomePage')
    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def RegisterPage(request):
    form = RegisterForm(request.POST or None)

    if request.POST and form.is_valid():
        # Check if the username is already in use
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'This username is already taken. Please choose a different one.')
        else:
            user = form.save()
            if user:
                # Log in the user
                login(request, user)
                return redirect('HomePage')

    context = {
        'form': form,
    }

    return render(request, "register.html", context)

@login_required(login_url='LoginPage')
def logout(request):
    auth.logout(request)
    return redirect('LoginPage')

from django.shortcuts import render
from django.http import HttpResponse
import random
from .models import Video

@login_required(login_url='LoginPage')
def HomePage(request):
    all_videos = Video.objects.all()
    
    # Check if there are at least 6 videos
    if len(all_videos) >= 6:
        random_videos = random.sample(list(all_videos), 6)
    else:
        # If there are less than 6 videos, use all available videos
        random_videos = list(all_videos)

    context = {
        'random_videos': random_videos,
    }

    return render(request, 'home.html', context)



class VideoUploadView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = 'videoupload.html'  # Replace 'your_template_name.html' with your actual template file
    form_class = VideoUploadForm
    success_url = reverse_lazy('HomePage')  # Replace 'success_page' with the URL name of your success page

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the current user as the user for the video
        return super().form_valid(form)

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videodetailedview.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get a list of random videos excluding the current video being viewed
        random_videos = Video.objects.exclude(pk=self.object.pk).order_by('?')[:5]
        
        context['random_videos'] = random_videos
        return context
    
@login_required
def ProfilePage(request, username):
    profile_user = get_object_or_404(User, username=username)
    videos = Video.objects.filter(user=profile_user)

    return render(request, 'profile.html', {'profile_user': profile_user, 'videos': videos})

@login_required
def delete_profile_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    # Check if the user has permission to delete the video
    if not video.user_can_delete(request.user):
        return HttpResponseForbidden("You don't have permission to delete this video.")

    profile_username = video.user.username

    # Delete the video
    video.delete()

    # Redirect back to the user's profile page
    return redirect('profile', username=profile_username)
@login_required(login_url='LoginPage')
def search_results(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    videos = Video.objects.filter(title__icontains=query)  # Customize the search query as needed

    return render(request, 'search_results.html', {'query': query, 'videos': videos})

@login_required(login_url='LoginPage')
def ListViewAdmin(request):
    videos = Video.objects.all()

    context = {
        'videos': videos
    }

    return render(request, 'admin/allvideos.html', context)
@user_passes_test(lambda u: u.is_staff, login_url='LoginPage')
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    if request.method == 'POST':
        # Debugging: Print statements
        print("Deleting video:", video.title)
        
        # Delete the video
        video.delete()

        # Debugging: Print statement after deletion
        print("Video deleted successfully.")

        return redirect('ModList')

    context = {
        'video': video
    }

    return render(request, 'home.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='LoginPage')
def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('ModList')
    else:
        form = VideoForm(instance=video)

    context = {
        'form': form,
        'video': video,
    }

    return render(request, 'admin/edit_video.html', context)

@login_required(login_url='LoginPage')
def edit_video_profile(request, pk):
    video = get_object_or_404(Video, pk=pk)

    # Check if the current user is the owner of the video
    if request.user != video.user:
        return HttpResponseForbidden("You don't have permission to edit this video.")

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('HomePage')
    else:
        form = VideoForm(instance=video)

    context = {
        'form': form,
        'video': video,
    }

    return render(request, 'edit_video_profile.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='LoginPage')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        # Debugging: Print statements
        
        # Delete the video
        user.delete()

        # Debugging: Print statement after deletion
        print("Video deleted successfully.")

        return redirect('ModList')

    context = {
        'user': user
    }

    return render(request, 'home.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='LoginPage')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('ModListUsers')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'admin/edit_user.html', context)


@login_required(login_url='LoginPage')
def ListViewAdminUsers(request):
    users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'admin/allusers.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='LoginPage')
def delete_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        # Redirect to the user list or a success page after deletion
    
    return redirect('ModListUsers')


@login_required(login_url='LoginPage')  # Ensure the user is logged in
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('HomePage')  # Redirect to the user's profile page
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)