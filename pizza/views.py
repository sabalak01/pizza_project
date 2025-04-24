from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Pizza
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


from .forms import PizzaFilterForm, PizzaForm
from .models import Pizza

def pizza_list(request):
    pizzas = Pizza.objects.all()
    form = PizzaFilterForm(request.GET or None)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if name:
            pizzas = pizzas.filter(name__icontains=name)
        if min_price is not None:
            pizzas = pizzas.filter(price__gte=min_price)
        if max_price is not None:
            pizzas = pizzas.filter(price__lte=max_price)

    return render(request, 'pizza/pizza_list.html', {'pizzas': pizzas, 'form': form})

def pizza_detail(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    return render(request, 'pizza/pizza_detail.html', {'pizza': pizza})


@login_required
def add_pizza_view(request):
    if not request.user.is_authenticated or not (request.user.is_admin() or request.user.is_manager()):
        raise PermissionDenied("У вас нет доступа к этой странице.")

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pizza_list')  
    else:
        form = PizzaForm()

    return render(request, 'pizza/add_pizza.html', {'form': form})

