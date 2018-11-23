from django.shortcuts import render
from .models import Product
from reviews.models import Review
# Create your views here.
def product_list(request):
    product=Product.objects.all()
    return render(request,"products/product_list.html",{'product':product})
    
def product_details(request,id):
    product=Product.objects.get(pk=id)
    # reviews=Review.objects.filter(product_id=id)
    return render(request, "products/product_details.html",{'product':product})