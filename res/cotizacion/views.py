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
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from core.erp.forms import *
from core.erp.mixins import ValidatePermissionRequiredMixin, IsSuperUserMixin
from core.erp.models import *
from django.contrib.auth.decorators import login_required



class CotizacionListView(LoginRequiredMixin, IsSuperUserMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cotizacion
    template_name = 'cotizacion/list.html'
    permission_required = 'erp.view_cotizacion'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Cotizacion.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            elif action == 'search_details_replacement':
                data = []
                position = 1
                for i in DetCotizacion.objects.filter(cotizacion_id=request.POST['id']):
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista Cotizaciones'
        context['create_url'] = reverse_lazy('erp:cotizacion_create')
        context['list_url'] = reverse_lazy('erp:cotizacion_list')
        context['entity'] = 'Cotizaciones'
        return context

class CotizacionCreateView(LoginRequiredMixin, IsSuperUserMixin, ValidatePermissionRequiredMixin, CreateView):

    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizacion/create.html'
    success_url = reverse_lazy('erp:cotizacion_list')
    success_url = reverse_lazy('index')
    permission_required = 'erp.add_cotizacion'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
        return JsonResponse(data, safe=False)




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Cotización'
        context['entity'] = 'Cotizaciones'
        context['list_url'] = reverse_lazy('erp:cotizacion_list')
        context['action'] = 'add'
        return context


class CotizacionUpdateView(LoginRequiredMixin, IsSuperUserMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizacion/create.html'
    success_url = reverse_lazy('erp:cotizacion_list')
    permission_required = 'erp.change_cotizacion'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # cotizacion = Cotizacion()
                    cotizacion = self.get_object()
                    cotizacion.date_joined = vents['date_joined']
                    cotizacion.cli_id = vents['cli']
                    cotizacion.money_id = vents['money']
                    cotizacion.pay_method_id = vents['pay_method']
                    cotizacion.subtotal = float(vents['subtotal'])
                    cotizacion.iva = float(vents['iva'])
                    cotizacion.total = float(vents['total'])
                    print(vents)
                    cotizacion.save()
                    cotizacion.detcotizacion_set.all().delete()
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
        return JsonResponse(data, safe=False)

    def get_details_replacement(self):
        data = []
        try:
            for i in DetCotizacion.objects.filter(cotizacion_id=self.get_object().id):
                item = i.repl.toJSON()
                item['stock'] = i.stock
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cotización'
        context['entity'] = 'Cotizaciones'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_replacement())
        return context


class CotizacionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Cotizacion
    template_name = 'cotizacion/delete.html'
    success_url = reverse_lazy('erp:cotizacion_list')
    permission_required = 'erp.delete_cotizacion'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cotización'
        context['entity'] = 'Cotizaciones'
        context['list_url'] = self.success_url
        return context


class CotizacionInvoiceView(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('cotizacion/invoice.html')
            context = {
                'cotizacion': Cotizacion.objects.get(pk=self.kwargs['pk']),
                'comp': {
                    'name': 'MAQTEC SPA',
                    'rut' : '76.831.125-0',
                    'phone': '9-82026231',
                    'address': 'LOS COPIHUES 0112, TEMUCO PADRE LAS CASAS',
                    'email_casa_matriz': 'MARIO.ULLOA@MAQTECCHILE.CL',
                    'giro': 'SERVICIO TECNICO',
                    
                },
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/LogoMAQTEC2.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:cotizacion_list'))