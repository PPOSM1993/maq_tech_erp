from datetime import datetime
from django.db import models
from django.forms import model_to_dict
# Create your models here.
from core.models import BaseModel
from crum import get_current_user
#from core.erp.choices import pay_methods

from django.core.validators import RegexValidator

class Category(BaseModel):
    
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Category, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Replacement(models.Model):
    
    code_replacement = models.CharField(max_length=150, verbose_name='Código', unique=True, null=True, blank=False)
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=False, null=True, blank=False)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio Final')
    location = models.CharField(max_length=150, verbose_name='Ubicación', null=True, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Replacement, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        verbose_name = 'Repuestos'
        verbose_name_plural = 'Repuestos'
        ordering = ['id']


class Money(models.Model):

    name = models.CharField(max_length=150, verbose_name='Tipo Moneda', unique=True, null=False, blank=False)

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Money, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        ordering = ['id']


class Clients(models.Model): 
    name = models.CharField(max_length=150, verbose_name='Cliente', unique=True)
    dni_regex = RegexValidator(
        regex=r'^0*(\d{1,3}(\.?\d{3})*)\-?([\dkK])$', message="Formato de Rut Incorrecto.")
    dni = models.CharField(
        validators=[dni_regex], max_length=12, unique=True, verbose_name='RUT')
    commercial_business = models.CharField(max_length=150, null=True, blank=True, verbose_name='Giro Comercial')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número de telefono debe tener el siguiente formato: '+999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True, verbose_name="Telefono") # validators should be a list
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ciudad')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='Email', unique=True)
    
    
    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return '{} / {}'.format(self.name, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item
    
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class PayMethods(models.Model):
    name = models.CharField(max_length=150, verbose_name='Método de Pago', unique=True, null=False, blank=False)


    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(PayMethods, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Metodo de Pago'
        verbose_name_plural = 'Metodos de Pago'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Clients, on_delete=models.PROTECT, verbose_name='Cliente')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Venta')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pay_method = models.ForeignKey(PayMethods, on_delete=models.PROTECT, verbose_name='Método de Pago')
    money = models.ForeignKey(Money, on_delete=models.PROTECT, verbose_name='Moneda')


    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['pay_method'] = self.pay_method.toJSON()
        item['money'] = self.money.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detcotizacion_set.all()]
        return item

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['id']


class DetSale(models.Model):
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    repl = models.ForeignKey(Replacement, on_delete=models.CASCADE, verbose_name='Repuesto(s)')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=0, verbose_name='Precio')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.repl.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['repl'] = self.repl.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Cotización'
        verbose_name_plural = 'Detalle Cotizaciones'
        ordering = ['id']

