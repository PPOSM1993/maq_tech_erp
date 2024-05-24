import json
import os
from re import template

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
#from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin, IsSuperUserMixin
from core.erp.models import *
from django.contrib.auth.decorators import login_required

class CotizacionCreateView(LoginRequiredMixin, IsSuperUserMixin, ValidatePermissionRequiredMixin, CreateView):

    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizacion/create.html'
    #success_url = reverse_lazy('erp:cotizacion_list')
    #success_url = reverse_lazy('index')
    #permission_required = 'erp.add_cotizacion'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    """def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_replacements':
                data = []
                repls = Replacement.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in repls:
                    item = i.toJSON()
                    item['value'] = i.name + " - " + i.code_replacement
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    cotizacion = Cotizacion()
                    cotizacion.date_joined = vents['date_joined']
                    cotizacion.cli_id = vents['cli']
                    cotizacion.money_id = vents['money']
                    cotizacion.pay_method_id = vents['pay_method']
                    cotizacion.subtotal = float(vents['subtotal'])
                    cotizacion.iva = float(vents['iva'])
                    cotizacion.total = float(vents['total'])
                    print(vents)
                    cotizacion.save()
                    
                    for i in vents['replacements']:
                        det = DetCotizacion()
                        det.cotizacion_id = cotizacion.id
                        det.repl_id = i['id']
                        det.stock = int(i['stock'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = "No ha ingresado a un ninguna opción"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)"""




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Cotización'
        context['entity'] = 'Cotizaciones'
        #context['list_url'] = reverse_lazy('erp:cotizacion_list')
        #context['action'] = 'add'
        return context