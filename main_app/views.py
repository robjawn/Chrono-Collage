from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Photo, PhotoContext, Profile
from .forms import UpdateUserForm, UpdateProfileForm, PhotoForm, PhotoContextForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'chronocollage'

@login_required
def profile(request):
  if request.method == 'POST':
    user_form = UpdateUserForm(request.POST, instance=request.user)
    profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Your profile has been updated successfully')
      return redirect('home')
  else:
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

  return render(request, 'profiles/profile.html', {'user_form': user_form, 'profile_form': profile_form })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid Registration - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-profile')

def profile_detail(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    photos = Photo.objects.filter(user=user)
    context = {
        'profile': profile,
        'photos': photos,
    }
    return render(request, 'profiles/profile_detail.html', context)

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def photos_index(request):
  photos = Photo.objects.all()
  photo_context = PhotoContext.objects.all()
  return render(request, 'photos/index.html', {'photos': photos, 'photo_context': photo_context})

def photos_detail(request, photo_id):
  photo = Photo.objects.get(id=photo_id)
  photo_context = PhotoContext.objects.get(id=photo_id)
  return render(request, 'photos/detail.html', {'photo': photo, 'photo_context': photo_context })

@login_required
def create_photo(request):
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        photo_context_form = PhotoContextForm(request.POST)
        if photo_form.is_valid() and photo_context_form.is_valid():
            photo_file = request.FILES.get('photo_file')
            if photo_file:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

                try:
                    s3.upload_fileobj(photo_file, BUCKET, key)
                    url = f"{S3_BASE_URL}{BUCKET}/{key}"
                    photo_context = photo_context_form.save()
                    photo = photo_form.save(commit=False)
                    photo.url = url
                    photo.photo_context = photo_context
                    photo.user = request.user
                    photo.save()
                except Exception as error:
                    print('something went wrong uploading to s3')
                    print(error)
                    return HttpResponse("An error occured while uploading to S3")
                return redirect('detail', photo_id=photo.id)
            else:
                return HttpResponse("No photo file was provided")
        else:
            return HttpResponse("The form is invalid")
    else:
        photo_form = PhotoForm()
        photo_context_form = PhotoContextForm()
        return render(request, 'main_app/photo_form.html', {'photo_form': photo_form, 'photo_context_form': photo_context_form})
  
@login_required
def photos_delete(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        photo_context = photo.photo_context
        photo.delete()
        photo_context.delete()
        return redirect('index')
    return render(request, 'main_app/photo_confirm_delete.html', {'photo': photo})

class PhotoUpdate(LoginRequiredMixin, UpdateView):
  model = Photo
  fields =['title', 'url']
  template_name = 'main_app/photo_update.html'
  def get_success_url(self):
        return reverse_lazy('detail', kwargs={'photo_id': self.object.id})

class PhotoContextUpdate(LoginRequiredMixin, UpdateView):
  model = PhotoContext
  fields = ['date','description','location','people']
  template_name = 'main_app/context_update.html'
  def get_success_url(self):
        return reverse_lazy('detail', kwargs={'photo_id': self.object.id})