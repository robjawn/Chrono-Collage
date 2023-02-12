from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Photo, PhotoContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# class Photo: 
#   def __init__(self, title, date, description, url):
#     self.title = title
#     self.date = date
#     self.description = description
#     self.url = url

# photos = [
#   Photo('Hindenburg Disaster', 1937, 'The Hindenburg disaster was an airship accident that occurred on May 6, 1937, in Manchester Township, New Jersey, United States.', 'https://upload.wikimedia.org/wikipedia/commons/1/1c/Hindenburg_disaster.jpg'),
#   Photo('Migrant Mother', 1936, 'A photo of Florence Owens Thompson, a mother raising her children amidst the Great Depression.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Lange-MigrantMother02.jpg/1024px-Lange-MigrantMother02.jpg'),
#   Photo('Earthrise', 1968, 'Photo of Earth taken from lunar orbit by astronaut William Anders.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/NASA-Apollo8-Dec24-Earthrise.jpg/1280px-NASA-Apollo8-Dec24-Earthrise.jpg'),
#   Photo('Salvador Dali Walking His Anteater', 1969, 'Surrealist painter Salvador Dali takes his pet for a stroll in Paris.', 'http://cdn8.openculture.com/wp-content/uploads/2015/05/dali-anteater1.jpg')
# ]

@login_required
def profile(request):
  return render(request, 'users/profile.html')

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
        photo_form = PhotoForm(request.POST)
        photo_context_form = PhotoContextForm(request.POST)
        if photo_form.is_valid() and photo_context_form.is_valid():
            photo_context = photo_context_form.save()
            photo = photo_form.save(commit=False)
            photo.photo_context = photo_context
            photo.user = request.user
            photo.save()
            return redirect('detail', photo_id=photo.id)
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