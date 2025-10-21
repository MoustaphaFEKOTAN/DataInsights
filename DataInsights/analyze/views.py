from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
import os


def analyze_file(request):
    """Vue pour traiter le formulaire et afficher les résultats"""
    form = UploadFileForm()
    result = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            result = process_file(uploaded_file)
            if 'error' in result:
                messages.error(request, result['error'])
                result = None
            else:
                messages.success(request, f"Fichier '{uploaded_file.name}' analysé avec succès !")

    return render(request, 'analyze.html', {'form': form, 'result': result})


def process_file(uploaded_file):
    """Analyse le fichier et retourne un dictionnaire de résultats"""
    fs = FileSystemStorage(location='media/uploads/')
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_path = fs.path(filename)

    try:
        # Lecture du fichier
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file_path)
        else:
            return {'error': "Format non supporté. Veuillez importer un fichier CSV ou Excel."}

        # Analyse
        lignes, colonnes = data.shape
        apercu = data.head(5)
        stats = data.describe().round(2)

        stats_labels = stats.index.tolist()
        stats_table = []
        for label, row in zip(stats_labels, stats.values.tolist()):
            stats_table.append({'label': label, 'row': row})

        resume = {
            'Nom_du_fichier': uploaded_file.name,
            'Nombre_de_lignes': lignes,
            'Nombre_de_colonnes': colonnes,
            'Colonnes': list(data.columns),
            'apercu': {
                'columns': list(apercu.columns),
                'values': apercu.values.tolist()
            },
            'stats': {
                'columns': list(stats.columns),
                'table': stats_table
            }
        }
        return resume

    except Exception as e:
        return {'error': f"Erreur lors du traitement : {str(e)}"}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
