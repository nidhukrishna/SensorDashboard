from django.db import models
from django.conf import settings

# Create your models here.

class SensorDataset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    raw_file = models.FileField(upload_to='raw_datasets/')
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ExtractedCycle(models.Model):
    dataset = models.ForeignKey(SensorDataset, related_name='cycles', on_delete=models.CASCADE)
    
    # Cycle Identifier
    cycle_number = models.IntegerField()
    
    # Raw Coordinates (Extracted from peaks/troughs)
    peak_time = models.FloatField(null=True, blank=True)
    peak_amplitude = models.FloatField(null=True, blank=True)
    trough_time = models.FloatField(null=True, blank=True)
    trough_amplitude = models.FloatField(null=True, blank=True)
    
    # Calculated Analytics (The actual Rise/Fall times)
    rise_time = models.FloatField(null=True, blank=True)
    fall_time = models.FloatField(null=True, blank=True)

    class Meta:
        # This ensures your cycles always return in chronological order
        ordering = ['cycle_number']

    def __str__(self):
        return f"Cycle {self.id} - Safe: {self.is_safe}"