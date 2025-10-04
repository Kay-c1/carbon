from django.db import models

# Create your models here.


class EnergyData(models.Model):
    date = models.DateField(auto_now_add=True)
    energy_used = models.FloatField()  # kWh
    co2_emission = models.FloatField()  # kg CO2

    def __str__(self):
        return f"{self.date} - {self.energy_used} kWh"
    
 

class EnergyData(models.Model):
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField(default=0)  # user input
    energy_consumed = models.FloatField(default=0.0)  # in kWh
    emission = models.FloatField(default=0.0)  # computed CO₂ in kg

    def __str__(self):
        return f"{self.date} - {self.emission:.2f} kg CO₂"

