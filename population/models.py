from django.db import models

class PopulationData(models.Model):
    date = models.DateField()
    population_count = models.IntegerField()
    nationality = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.date} - {self.population_count} - {self.nationality} "
