import pandas as pd
from django.conf import settings
from pathlib import Path
from django.shortcuts import render, redirect
from .forms import ExperimentForm, SignalDataForm, CSVUploadForm
from .models import Experiment, SignalData


def index(request):
    return render(request, 'index.html')


def create_experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('experiment_list')
    else:
        form = ExperimentForm()
    return render(request, 'create_experiment.html', {'form': form})


def experiment_list(request):
    experiments = Experiment.objects.all()
    return render(request, 'experiment_list.html', {'experiments': experiments})


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            experiment = form.cleaned_data['experiment']
            csv_file = form.cleaned_data['csv_file']
            threshold = form.cleaned_data['threshold']
            # Save the uploaded CSV file to the data directory
            csv_path = settings.DATA_DIR / csv_file.name
            with open(csv_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
            return redirect('process_csv', experiment_id=experiment.id, csv_path=csv_path, threshold=str(threshold))
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def process_csv(request, experiment_id, csv_path, threshold):
    experiment = Experiment.objects.get(id=experiment_id)
    data = pd.read_csv(csv_path, delimiter='\t')  # Read CSV with tab delimiter
    columns = data.columns.tolist()

    # Convert the threshold from str to float
    threshold = float(threshold)

    if request.method == 'POST':
        signal_column = request.POST['signal_column']
        signal_data = pd.to_numeric(data[signal_column],
                                    errors='coerce')  # Convert to numeric, invalid parsing will be set as NaN
        normalized_signal = normalize_data(signal_data.dropna())  # Drop NaNs before normalization
        decoded_data = decode_signal(normalized_signal, threshold)

        signal_data_instance = SignalData(
            experiment=experiment,
            signal=normalized_signal.to_json(),
            decoded_data=decoded_data,
            signal_column=signal_column,
            threshold=threshold
        )
        signal_data_instance.save()
        return redirect('signal_data_list')

    return render(request, 'process_csv.html',
                  {'columns': columns, 'experiment': experiment, 'csv_path': csv_path, 'threshold': threshold})


def signal_data_list(request):
    signal_data = SignalData.objects.all()
    return render(request, 'signal_data_list.html', {'signal_data': signal_data})


def normalize_data(signal_data):
    min_val = signal_data.min()
    max_val = signal_data.max()
    return (signal_data - min_val) / (max_val - min_val)


def decode_signal(signal_data, threshold):
    decoded_data = ""
    for signal in signal_data:
        if signal > threshold:
            decoded_data += '1'
        else:
            decoded_data += '0'
    return decoded_data
