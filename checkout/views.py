from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from products.models import Product
from .forms import MakePaymentForm,OrderForms
from .models import OrderLineItem
from django.conf import settings
import stripe 
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def get_cart_item_and_total(cart):
    
    
    grd_total=0
    cart_items = []
    for product_id, quantity in cart.items():
        
        product = get_object_or_404(Product, pk=product_id)
        grd_total+=product.price * quantity
        # print(quantity)
    
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'sku': product.sku,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'stock': product.stock,
            'quantity': quantity,
            'total': product.price * quantity,
            
        })    
    return {'cart_items': cart_items,'grd_total':grd_total}  
    

def checkout_show(request):
    cart = request.session.get('cart', {})
    cart_item_and_total=get_cart_item_and_total(cart)
    payment_form=MakePaymentForm()
    order_form = OrderForms()
    context={'payment_form':payment_form,'order_form':order_form,'publishable':settings.STRIPE_PUBLISHABLE_KEY}
    context.update(cart_item_and_total)
    return render(request, "checkout/checkout_show.html",context)
    
def submit_payment(request):
    
    cart = request.session.get('cart', {})
    cart_item_and_total=get_cart_item_and_total(cart)
    
    payment_form=MakePaymentForm(request.POST)
    form=OrderForms(request.POST)
    
    if form.is_valid() and payment_form.is_valid():
         #Saves the order to the DB
        order = form.save()
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            line_item = OrderLineItem()
            line_item.product_id = product_id
            line_item.quantity = quantity
            line_item.order = order
            line_item.save()
        
        # Grab the money and run
        total = cart_item_and_total['grd_total']
        stripe_token=payment_form.cleaned_data['stripe_id']

        try:

            total_in_cent = int(total*100)
            customer = stripe.Charge.create(
                amount=total_in_cent,
                currency="EUR",
                description="Dummy Transaction",
                card=stripe_token,
            )

        except stripe.error.CardError:
            print("Declined")
            messages.error(request, "Your card was declined!")

        if customer.paid:
            print("Paid")
            messages.error(request, "You have successfully paid")
         
         #clear the cart       
        del request.session['cart']
        
        return redirect("/")
        
    
    
    
    
    
    