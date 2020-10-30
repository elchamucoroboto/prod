from django.db import models

# Create your models here.
class Operacion(models.Model):
    monto = models.FloatField()
    metodo = models.CharField(max_length=200)
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField('fecha creado')

    

    def __str__(self):
        result = str(self.monto) + '||' + str(self.motivo) + '||' + str(self.metodo) + '||' + str(self.fecha)
        return result