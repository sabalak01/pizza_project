from django import forms
from .models import Order, OrderItem
from pizza.models import Pizza
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']  

        widgets = {
            'address': forms.Textarea(attrs={'placeholder': 'Укажите адрес доставки'}),
        }

        
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['pizza', 'quantity']

        widgets = {
            'pizza': forms.Select(),
            'quantity': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Количество пиццы'}),
        }
        
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть положительным числом.")
        return quantity

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
    widgets = {
        'status': forms.Select(choices=Order.STATUS_CHOICES),
    }