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