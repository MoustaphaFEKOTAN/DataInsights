from django.shortcuts import render
from .forms import UploadFileForm

def home(request):
    form = UploadFileForm()
    return render(request, 'home.html', {'form': form})
