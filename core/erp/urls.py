from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.replacement.views import *
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import DashboardView
#from core.erp.views.sale.views import *
from core.erp.views.pay_methods.views import *
from core.erp.views.cotizacion.views import *
from core.erp.views.money.views import *


app_name = 'erp'

urlpatterns = [
    #Category
    path('category/list/', CategoryListView.as_view(), name="category_list"),
    path('category/add/', CategoryCreateView.as_view(), name="category_create"),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name="category_update"),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name="category_delete"),

    #Replacement
    path('replacement/list/', ReplacementListView.as_view(), name="replacement_list"),
    path('replacement/add/', ReplacementCreateView.as_view(), name="replacement_create"),
    path('replacement/update/<int:pk>/', ReplacementUpdateView.as_view(), name="replacement_update"),
    path('replacement/delete/<int:pk>/', ReplacementDeleteView.as_view(), name="replacement_delete"),

    #Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    #Money
    path('money/list', MoneyListView.as_view(), name="money_list"),
    path('money/add/', MoneyCreateView.as_view(), name="money_create"),
    path('money/update/<int:pk>/', MoneyUpdateView.as_view(), name="money_update"),
    path('money/delete/<int:pk>/', MoneyDeleteView.as_view(), name="money_delete"),


    #Pay Methods
    path('pay_methods/list/', PayMethodListView.as_view(), name="pay_methods_list"),
    path('pay_methods/add/', PayMethodsCreateView.as_view(), name="pay_methods_create"),
    path('pay_methods/update/<int:pk>/', PayMethodsUpdateView.as_view(), name="pay_methods_update"),
    path('pay_methods/delete/<int:pk>/', PayMethodsDeleteView.as_view(), name="pay_methods_delete"),


    #Customer
    path('client/list/', ClientListView.as_view(), name="client_list"),
    path('client/add/', ClientCreateView.as_view(), name="client_create"),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name="client_update"),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name="client_delete"),

    #Cotizaciones
    path('cotizacion/list/', CotizacionListView.as_view(), name="cotizacion_list"),
    path('cotizacion/add/', CotizacionCreateView.as_view(), name='cotizacion_create'),
    path('cotizacion/update/<int:pk>/', CotizacionUpdateView.as_view(), name='cotizacion_update'),
    path('cotizacion/delete/<int:pk>/', CotizacionDeleteView.as_view(), name="cotizacion_delete"),
    path('cotizacion/invoice/pdf/<int:pk>/', CotizacionInvoiceView.as_view(), name="cotizacion_invoice_pdf"),

]