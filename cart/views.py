from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from products.models import Product
import json
# Create your views here.
def add_to_cart(request):
    product_id=request.POST['product']
    quantity=int(request.POST['quantity'])
    cart= request.session.get('cart',{})
    cart[product_id]=cart.get(product_id,0)+quantity
    request.session['cart']=cart
    
    # return HttpResponse("quantity"+quantity+",product"+product_id)
    # return HttpResponse(json.dumps(cart))
    return redirect("/")
    
# def view_cart(request):
#     cart= request.session.get('cart',{})
#     # return HttpResponse(json.dumps(cart))
#     return render(request,"cart/view_cart.html")


def view_cart(request):
    cart = request.session.get('cart', {})
    
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
    

    return render(request, "cart/view_cart.html", {'cart_items': cart_items,'grd_total':grd_total})
    
def remove_item(request,id):
    cart=request.session.get('cart',{})
    
    del cart[str(id)]
    request.session['cart']=cart
    return redirect("view_cart")