from django.forms import ModelForm
from django.forms import *
from core.erp.models import *

class CategoryForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre Categoría',
                    'class': 'form-control form-control-sm',
                    'autofocus': True
                }
            )
        }
        
        exclude = ['user_updated', 'user_creation']
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ReplacementForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Replacement
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Repuesto',
                    'class': 'form-control form-control-md'
                }
            ),
            'cat': Select(attrs={
                'class': 'form-select-md select2',
            }),
            'code_replacement': TextInput(
                attrs={
                    'placeholder': 'Código Respuesto',
                    'class': 'form-control form-control-md'
                }
            ),
            'stock': TextInput(
                attrs={
                    'placeholder': '',
                    "type": "number",
                    'class': 'form-control form-control-md',
                    'min':'0'
                }
            ),
            'pvp': TextInput(
                attrs={
                    'placeholder': '',
                    "type": "number",
                    'class': 'form-control form-control-md',
                    'min':'0'
                }
            ),
            
            """'precio_compra': TextInput(
                attrs={
                    'placeholder': '',
                    "type": "number",
                    'class': 'form-control form-control-md'
                }
            ),"""
        
            
            'location': TextInput(
                attrs={
                    'placeholder': 'Ubicación',
                    "type": "text",
                    'class': 'form-control form-control-sm',
                }
            )
            
            
                        
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class MoneyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Money
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre Moneda ($)',
                    'class': 'form-control form-control-sm',
                    'autofocus': True
                }
            )
        }
        
        exclude = ['user_updated', 'user_creation']
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PayMethodsForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = PayMethods
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Medio de Pago',
                    'class': 'form-control form-control-sm',
                    'autofocus': True
                }
            )
        }
        
        exclude = ['user_updated', 'user_creation']
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientsForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Nombre Cliente',
                    'class': 'form-control form-control-sm'
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese RUT',
                    'class': 'form-control form-control-sm'
                }
            ),
            'commercial_business': TextInput(
                attrs={
                    'placeholder': 'Giro Comercial',
                    'class': 'form-control form-control-sm'
                }
            ),
            'phone': TextInput(
                attrs={
                    'placeholder': 'Ingrese Número de Contacto',
                    'class': 'form-control form-control-sm'
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese Email',
                    'class': 'form-control form-control-sm'
                }
            ),
            
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese Dirección',
                    'class': 'form-control form-control-sm'
                }
            ),
            'city': TextInput(
                attrs={
                    'placeholder': 'Ingrese Ciudad',
                    'class': 'form-control form-control-sm'
                }
            ),
        }
        
        exclude = ['user_updated', 'user_creation']
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CotizacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['select'] = 'off'
        self.fields['cli'].widget.attrs['class'] = 'form-control select2'
        self.fields['money'].widget.attrs['class'] = 'form-control select2'
        self.fields['pay_method'].widget.attrs['class'] = 'form-control select2'

    class Meta:
        model = Cotizacion
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
                
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input form-control-md',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control form-control-md',
                'readonly': True
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control form-control-md',
            }),
            'pay_method': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'money': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control form-control-md',
            })
        }

    def save(self, comit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data