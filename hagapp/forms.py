from django import forms
from .models import Experiment, SignalData

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['title', 'description']

class CSVUploadForm(forms.Form):
    experiment = forms.ModelChoiceField(queryset=Experiment.objects.all())
    csv_file = forms.FileField()
    threshold = forms.FloatField(initial=0.5, min_value=0, max_value=1)

class SignalDataForm(forms.ModelForm):
    class Meta:
        model = SignalData
        fields = ['experiment', 'signal', 'decoded_data', 'signal_column', 'threshold']
        widgets = {
            'signal': forms.HiddenInput(),
            'decoded_data': forms.HiddenInput(),
            'signal_column': forms.HiddenInput(),
            'threshold': forms.HiddenInput(),
        }
