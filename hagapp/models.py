from django.db import models

class Experiment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_conducted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SignalData(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    signal = models.TextField()
    decoded_data = models.TextField()
    signal_column = models.CharField(max_length=200, default="")
    threshold = models.FloatField(default=0.5)

    def __str__(self):
        return f"Signal Data for {self.experiment.title}"
