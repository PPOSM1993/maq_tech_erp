from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.erp.mixins import IsSuperUserMixin, ValidatePermissionRequiredMixin
from core.erp.models import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.erp.forms import PayMethodsForm


from django.contrib.auth.mixins import LoginRequiredMixin

class PayMethodListView(LoginRequiredMixin, IsSuperUserMixin, ValidatePermissionRequiredMixin, ListView):
    model = PayMethods 
    template_name = "pay_methods/list.html"
    permission_required = 'erp.view_pay_method'
    
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in PayMethods.objects.all():
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
        context['title'] = 'Listado Medios de Pago'
        context['create_url'] = reverse_lazy('erp:pay_methods_create')
        context['list_url'] = reverse_lazy('erp:pay_methods_list')
        context['entity'] = 'Categorias'
        return context

class PayMethodsCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = PayMethods
    form_class = PayMethodsForm
    template_name = 'pay_methods/create.html'
    success_url = reverse_lazy('erp:pay_methods_list')
    permission_required = 'erp.add_pay_methods'
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
        context['title'] = 'Creación Medio de Pagoo'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class PayMethodsUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = PayMethods
    form_class = PayMethodsForm
    template_name = 'pay_methods/create.html'
    success_url = reverse_lazy('erp:pay_methods_list')
    permission_required = 'erp.change_pay_methods'
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
        context['title'] = 'Actualización Medio de Pago'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class PayMethodsDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = PayMethods
    template_name = 'pay_methods/delete.html'
    success_url = reverse_lazy('erp:pay_methods_list')
    permission_required = 'erp.delete_pay_methods'
    url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
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
        context['title'] = 'Eliminar Medio de Pago'
        context['entity'] = 'Medios de Pago'
        context['list_url'] = reverse_lazy('erp:pay_methods_list')
        return context