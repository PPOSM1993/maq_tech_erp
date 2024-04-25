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