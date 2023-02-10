from django.shortcuts import render


from django.http import HttpResponse

class Photo: 
  def __init__(self, title, date, description, url):
    self.title = title
    self.date = date
    self.description = description
    self.url = url

photos = [
  Photo('Hindenburg Disaster', 1937, 'The Hindenburg disaster was an airship accident that occurred on May 6, 1937, in Manchester Township, New Jersey, United States.', 'https://upload.wikimedia.org/wikipedia/commons/1/1c/Hindenburg_disaster.jpg'),
  Photo('Migrant Mother', 1936, 'A photo of Florence Owens Thompson, a mother raising her children amidst the Great Depression.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Lange-MigrantMother02.jpg/1024px-Lange-MigrantMother02.jpg'),
  Photo('Earthrise', 1968, 'Photo of Earth taken from lunar orbit by astronaut William Anders.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/NASA-Apollo8-Dec24-Earthrise.jpg/1280px-NASA-Apollo8-Dec24-Earthrise.jpg')
]


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def photos_index(request):
  return render(request, 'photos/index.html', {'photos': photos})