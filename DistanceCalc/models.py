from django.db import models

# Create your models here.
class Distance(models.Model):
    source_url = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Distance of {self.distance} from {self.source_url} server to {self.destination}."
