from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime, localdate
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.forms import formset_factory, inlineformset_factory
from Sellers.forms import OrderItemForm, OrderForm, OrderItemFormset
from Sellers.models import Order, OrderItem, Log
from Sellers.utils import render_to_pdf
from Warehouse.models import Product
from django.contrib.auth.decorators import login_required



@login_required
def log(request):
    if request.method == "POST":
        searched = request.POST['searched']
        log = Log.objects.filter(date_created=datetime.date(searched)).order_by('-id')

        context = {
            'searched': searched,
            'log': log,
        }
        return render(request, 'seller/log.html', context)
    else:
        return render(request, 'seller/log.html', {})


def search_log_by_date(request):
    return render(request, 'seller/search_log.html')


class CreateOrder(LoginRequiredMixin, CreateView):
    template_name = "seller/create_order.html"
    form_class = OrderForm

    def get_success_url(self):
        return reverse_lazy('addorderitems', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.status = 'PENDING'
        form.instance.seller = self.request.user
        form.save()
        return super().form_valid(form)


def search_order_by_date(request):
    return render(request, 'seller/search_orders.html')


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'seller/detail_order.html'
    context_object_name = 'order'


    #
    # def get_success_url(self):
    #     return reverse_lazy('pdf', kwargs={'pk': self.object.pk})

@login_required
def add_orderitems(request, pk):
    context = {}
    obj = get_object_or_404(Order, pk=pk)
    orderItemFormset = inlineformset_factory(Order, OrderItem, fields=('item', 'quantity',), extra=obj.num_of_product)

    if request.method == 'POST':
        orderItems = orderItemFormset(request.POST, instance=obj)

        if orderItems.is_valid():
            items = orderItems.save(commit=False)
            completed = True

            for orderItem in items:
                id = orderItem.item.pk
                product = get_object_or_404(Product, pk=id)
                if orderItem.quantity > product.quantity:
                    completed = False
                    messages.error(request, f"We don't Currently have the quantity available for {orderItem.item}")

            count = 0

            if completed:
                for item in items:
                    id = item.item.pk
                    product = get_object_or_404(Product, pk=id)
                    product.quantity -= item.quantity
                    product.save()
                    completed = True
                    item.seller = request.user

                    count += 1

                    if count == len(items):
                        obj.completed = True
                        obj.status = 'COMPLETED'
                        obj.save()
                    item.save()
                    if product.quantity == 0:
                        product.availability = False
                        product.save()

            if completed:
                return redirect('orderdetail', pk=pk)

    context['formset'] = orderItemFormset
    context['obj'] = obj

    return render(request, "seller/add_orderitems.html", context)

@login_required
def home(request, since=None):
    orders = Order.objects.filter(created_at__day=localdate().today().day, completed=True)
    cost = 0

    today = datetime.today()
    ord = Order.objects.filter(created_at__month=today.month)
    data = []
    label = []

    dat = datetime.now()
    for x in range(1, 32):
        month_order = ord.filter(created_at__day=x).count()
        data.append(month_order)

        label.append(f'{dat.strftime("%b")} {x}')
        if x == datetime.today().day:
            break

    for order in orders:
        cost += order.total_price
    order = Order.objects.filter(created_at__day=localdate().today().day, completed=True).count()
    context = {'cost': cost, 'order': order, 'orders_made': orders,'labels':label,'data':data}
    return render(request, 'home.html', context)

@login_required
def search_order_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        orders = Order.objects.filter(created_at=searched, completed=True).order_by('-id')

        context = {
            'searched': searched,
            'orders': orders,
        }
        return render(request, 'seller/order_result.html', context)
    else:
        return render(request, 'seller/order_result.html', {})


def Print_Receipt(request, pk):
    template_name = "seller/print_receipt.html"
    receipt = get_object_or_404(Order, pk=pk)
    # user = request.user.get_username()

    return render_to_pdf(
        template_name,
        {
            "receipt": receipt,

        },
    )
