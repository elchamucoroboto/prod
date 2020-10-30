from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Operacion
from datetime import date
from django.contrib.auth.decorators import login_required
from .forms import opForm, fechaForm
from django.utils import timezone
import datetime



# Create your views here.
@login_required(login_url='/login')
def index(request):

    listZelle = [0]
    listPunto = [0]
    listEfectivoD = [0]
    listEfectivoBS = [0]
    listValesD = [0]
    listValesBs = [0]
    fondoCajaD = 0.00
    fondoCajaBs = 0.00
    tasa_del_dia = 0.00001
    sumValesD = 0.00
    sumValesBs = 0.00
    sumZelle = 0.00
    sumPunto = 0.00
    sumEfectivoD = 0.00
    sumEfectivoBS = 0.00
    venta_bolivares_dolares = 0.00
    venta_total_dolares = 0.00
    venta_total_bolivares = 0.00
    venta_aprox = 0.0
    

    def floatToNegative(monto):

        monto = '-'+str(monto)
        monto = float(monto)
        return monto

    from .forms import opForm

    if request.method == 'GET':
        form = opForm
        today = date.today()
        operations = Operacion.objects.filter(fecha__year=today.year, fecha__month=today.month, fecha__day=today.day)
        template = loader.get_template('caja/index.html')



        #listZelle = [0]
        #listPunto = [0]
        #listEfectivoD = [0]
        #listEfectivoBS = [0]
        #fondoCajaD = 0.00
        #fondoCajaBs = 0.00
        #sumZelle = 0.00
        #sumPunto = 0.00
        #sumEfectivoD = 0.00
        #sumEfectivoBS = 0.00
        #venta_total_dolares = 0.00
        #venta_total_bolivares = 0.00
     

        for op in operations:
            if 'ZELLE' in op.metodo:
                listZelle.append(op.monto)
                sumZelle = sum(listZelle)

        for op in operations:
            if 'PUNTO' in op.metodo:
                listPunto.append(op.monto)
                sumPunto = sum(listPunto)

        for op in operations:
            if 'DOLARES EN EFECTIVO' in op.metodo:
                listEfectivoD.append(op.monto)
                sumEfectivoD = sum(listEfectivoD)

        for op in operations:
            if 'BOLIVARES EN EFECTIVO' in op.metodo:
                listEfectivoBS.append(op.monto)
                sumEfectivoBS = sum(listEfectivoBS)

        for op in operations:
            if 'FONDO CAJA BOLIVARES' == op.metodo:
                fondoCajaBs = op.monto

        for op in operations:
            if 'FONDO CAJA DOLARES' == op.metodo:
                fondoCajaD = op.monto

        for op in operations:
            if 'DOLAR DEL DIA' == op.metodo:
                tasa_del_dia = op.monto

        for op in operations:
            if 'VALE EN DOLARES' in op.metodo:
                listValesD.append(op.monto)
                sumValesD = sum(listValesD)



 


        #TOTALES
        venta_total_bolivares = sumEfectivoBS+sumPunto
        venta_total_dolares = sumZelle+sumEfectivoD
        venta_bolivares_dolares = venta_total_bolivares / tasa_del_dia
        venta_aprox = venta_total_dolares + venta_bolivares_dolares
        dolares_en_caja = fondoCajaD + sumEfectivoD + sumValesD 
        bs_en_caja = fondoCajaBs + sumEfectivoBS + sumValesBs

        context = {'operations': operations,
                    'form': form,
                    'sumZelle': sumZelle,
                    'sumPunto': sumPunto,
                    'sumEfectivoD': sumEfectivoD,
                    'sumEfectivoBS': sumEfectivoBS,
                    'venta_total_bolivares': venta_total_bolivares,
                    'venta_total_dolares':venta_total_dolares,
                    'fondoCajaD':fondoCajaD,
                    'fondoCajaBs':fondoCajaBs,
                    'dolares_en_caja': dolares_en_caja,
                    'bs_en_caja': bs_en_caja,
                    'sumValesD': sumValesD,
                    'venta_bolivares_dolares': venta_bolivares_dolares,
                    'tasa_del_dia' : tasa_del_dia,
                    'venta_aprox' : venta_aprox
                    }

        template = loader.get_template('caja/index.html')
        return HttpResponse(template.render(context, request))
    
    else:

        form = opForm(request.POST)
        if form.is_valid():

            monto = form.cleaned_data['monto']
            metodo = form.cleaned_data['metodo']
            motivo = form.cleaned_data['motivo']
            motivo = motivo.upper()

            if 'DEVOLUCION' in motivo or 'VALE' in metodo:
                monto = floatToNegative(monto)

            if 'FONDO CAJA BOLIVARES' == metodo:
                fondoCajaBs = monto
            
            if 'FONDO CAJA DOLARES' == metodo:
                fondoCajaD = monto

            if 'DOLAR DEL DIA' == metodo:
                tasa_del_dia = monto







                
            op = Operacion(monto=monto, metodo=metodo,motivo=motivo,fecha=date.today()) #()timezone.now()
            op.save()

        return HttpResponseRedirect('/')
        


@login_required(login_url='/login')
def informes(request):

    listZelle = [0]
    listPunto = [0]
    listEfectivoD = [0]
    listEfectivoBS = [0]
    fondoCajaD = 0.00
    fondoCajaBs = 0.00
    sumZelle = 0.00
    sumPunto = 0.00
    sumEfectivoD = 0.00
    sumEfectivoBS = 0.00
    venta_total_dolares = 0.00
    venta_total_bolivares = 0.00
    tasa_del_dia = 0.0
    
    if request.method == 'POST':
        form = fechaForm(request.POST)
        if form.is_valid():

            desde = form.cleaned_data['desde'] 
            hasta = form.cleaned_data['hasta']

            #desde = str(desde)
            #desde = desde.replace('-', ',')
            #hasta = str(hasta)
            #hasta = hasta.replace('-', ',')

            operations = Operacion.objects.filter(fecha__date__range=[desde, hasta])

            for op in operations:
                if 'ZELLE' in op.metodo:
                    listZelle.append(op.monto)
                    sumZelle = sum(listZelle)

            for op in operations:
                if 'PUNTO' in op.metodo:
                    listPunto.append(op.monto)
                    sumPunto = sum(listPunto)

            for op in operations:
                if 'DOLARES EN EFECTIVO' in op.metodo:
                    listEfectivoD.append(op.monto)
                    sumEfectivoD = sum(listEfectivoD)

            for op in operations:
                if 'BOLIVARES EN EFECTIVO' in op.metodo:
                    listEfectivoBS.append(op.monto)
                    sumEfectivoBS = sum(listEfectivoBS)

            for op in operations:
                if 'FONDO CAJA BOLIVARES' == op.metodo:
                    fondoCajaBs = op.monto

            for op in operations:
                if 'FONDO CAJA DOLARES' == op.metodo:
                    fondoCajaD = op.monto



            

            
            template = loader.get_template('caja/informes.html')
            context = {'operations': operations,
            'form':form,
            'sumZelle': sumZelle,
            'sumPunto': sumPunto,
            'sumEfectivoD': sumEfectivoD,
            'sumEfectivoBS': sumEfectivoBS,
            'venta_total_bolivares': venta_total_bolivares,
            'venta_total_dolares':venta_total_dolares,
            'fondoCajaD':fondoCajaD,
            'fondoCajaBs':fondoCajaBs,}

            return HttpResponse(template.render(context, request))

    else:
    
        form = fechaForm
    
        template = loader.get_template('caja/informes.html')
        context = {'form': form }
        return HttpResponse(template.render(context, request))


'''
        today = date.today()
        operations = Operacion.objects.filter(fecha__year=today.year, fecha__month=today.month, fecha__day=today.day)

        listZelle = [0]
        listPunto = [0]
        listEfectivoD = [0]
        listEfectivoBS = [0]
        fondoCajaD = 0.00
        fondoCajaBs = 0.00
        sumZelle = 0.00
        sumPunto = 0.00
        sumEfectivoD = 0.00
        sumEfectivoBS = 0.00
        venta_total_dolares = 0.00
        venta_total_bolivares = 0.00

        def currencyFormat(monto):
            currency = "{:,.2f}".format(monto)
            return currency

        for op in operations:
            if 'ZELLE' in op.metodo.upper():
                listZelle.insert(0, op.monto)
                sumZelle = sum(listZelle)
                

            if 'PUNTO' in op.metodo.upper():
                listPunto.insert(0, op.monto)
                sumPunto = sum(listPunto)

            if 'DOLARES EFECTIVO' in op.metodo.upper():
                listEfectivoD.insert(0, op.monto)
                sumEfectivoD = sum(listEfectivoD)
                

            if 'BOLIVARES EFECTIVO' in op.metodo.upper():
                listEfectivoBS.insert(0, op.monto)
                sumEfectivoBS = sum(listEfectivoBS)

            if 'FONDO DE CAJA DOLARES' in op.metodo.upper():
                fondoCajaD = op.monto

            if 'FONDO DE CAJA BOLIVARES' in op.metodo.upper():
                fondoCajaBs = op.monto

            venta_total_dolares = sumZelle + sumEfectivoD
            venta_total_bolivares = sumPunto + sumEfectivoBS


        template = loader.get_template('caja/index.html')
        context = {
            'operations': operations,
            'sumZelle' : currencyFormat(sumZelle), 
            'sumPunto' : currencyFormat(sumPunto), 
            'sumEfectivoBS' : currencyFormat(sumEfectivoBS) , 
            'venta_total_dolares' : currencyFormat(venta_total_dolares), 
            'venta_total_bolivares' : currencyFormat(venta_total_bolivares), 
            'sumEfectivoD' : currencyFormat(sumEfectivoD), 
            'fondoCajaD' : currencyFormat(fondoCajaD), 
            'fondoCajaBs' : currencyFormat(fondoCajaBs),
        }
        return HttpResponse(template.render(context, request))
        '''
