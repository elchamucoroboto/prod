from django import forms


class opForm(forms.Form):
    monto = forms.FloatField(required=True)
    metodo = forms.ChoiceField(choices=[("PUNTO", "PUNTO DE VENTA"), ("BOLIVARES EN EFECTIVO", "BOLIVARES EN EFECTIVO"),("DOLARES EN EFECTIVO", "DOLARES EN EFECTIVO"),("ZELLE", "ZELLE"),("FONDO CAJA BOLIVARES", "FONDO CAJA BOLIVARES"),("FONDO CAJA DOLARES", "FONDO CAJA DOLARES"),("VALE EN DOLARES","VALE EN DOLARES"),("VALE EN BOLIVARES","VALE EN BOLIVARES")], required=True)
    motivo = forms.CharField(required=True)

class fechaForm(forms.Form):
    desde = forms.DateField(required=True)
    hasta = forms.DateField(required=True)