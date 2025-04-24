from django import forms
from .models import Pizza, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название категории'})
        }


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название пиццы'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class PizzaFilterForm(forms.Form):
    name = forms.CharField(label='Название', required=False)
    min_price = forms.DecimalField(label='Цена от', required=False, min_value=0)
    max_price = forms.DecimalField(label='Цена до', required=False, min_value=0)
