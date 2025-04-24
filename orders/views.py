from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemForm, OrderStatusForm
from .models import Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)

        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user  # Пользователь, который создает заказ
            order.save()

            order_item = order_item_form.save(commit=False)
            order_item.order = order
            order_item.price = order_item.pizza.price  # Устанавливаем цену пиццы
            order_item.save()

            total_price = sum(item.get_total_price() for item in order.items.all())
            order.total_price = total_price
            order.save()

            return redirect('order_detail', order_id=order.id)

    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()

    return render(request, 'orders/create_order.html', {
        'order_form': order_form,
        'order_item_form': order_item_form
    })



# Проверка, является ли пользователь администратором или менеджером
def is_admin_or_manager(user):
    return user.is_admin() or user.is_manager()

@login_required
def order_list(request):
    # Получаем все заказы пользователя
    if request.user.is_admin() or request.user.is_manager():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
@user_passes_test(is_admin_or_manager)
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')  
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'orders/change_order_status.html', {'form': form, 'order': order})


from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user and not request.user.is_admin() and not request.user.is_manager():
        return redirect('order_list')  

    return render(request, 'orders/order_detail.html', {'order': order})
