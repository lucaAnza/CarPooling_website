from django.db import models

class Car(models.Model):
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=15)
    km = models.IntegerField(default=-1)
    last_inspection_date = models.DateField(default=None)
    def __str__(self):
        out = self.model + " di " + self.autore
        if self.data_prestito == None:
            out += "Nessuna revisione"
        return out

    class Meta:
        verbose_name_plural = "Cars"
