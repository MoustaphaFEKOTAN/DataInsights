from django.shortcuts import render
from .forms import UploadFileForm



def analyze_file(request):
    result = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # ici tu peux appeler ta fonction d'analyse
            result = process_file(uploaded_file)

    
    return render(request, 'analyze.html', {'form': form, 'result': result})