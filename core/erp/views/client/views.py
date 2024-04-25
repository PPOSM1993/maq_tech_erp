from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.erp.mixins import IsSuperUserMixin, ValidatePermissionRequiredMixin
from core.erp.models import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin



from django.contrib.auth.mixins import LoginRequiredMixin

class ClientListView(LoginRequiredMixin, IsSuperUserMixin, ListView):
    model = Clients
    template_name = 'client/list.html'
    permission_required = 'erp.view_client'
    
    
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
                for i in Clients.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position+=1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Clientes'
        context['create_url'] = reverse_lazy('erp:client_create')
        context['list_url'] = reverse_lazy('erp:client_list')
        context['entity'] = 'Clientes'
        return context

class ClientCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Clients
    form_class = ClientsForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('erp:client_list')
    permission_required = 'erp.add_client'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado a un ninguna opción"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class ClientUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    
    model = Clients
    form_class = ClientsForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('erp:client_list')
    permission_required = 'erp.change_client'
    url_redirect = success_url
    

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No ha ingresado a un ninguna opción"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ClientDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Clients
    template_name = 'client/delete.html'
    success_url = reverse_lazy('erp:client_list')
    permission_required = 'erp.delete_client'
    url_redirect = success_url
    
    success_url = reverse_lazy('erp:client_list')
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Eliminar Client'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:category_list')
        return context