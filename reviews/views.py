from django.shortcuts import render,redirect
from .models import Review
from .forms import ReviewForm
from products.views import product_details
# Create your views here.

def make_review(request,id):
    if request.method=="POST":
        form=ReviewForm(request.POST)
        rev=form.save(commit=False)
        rev.author=request.user
        rev.product_id=id
        rev.save()
        return redirect(product_details,id=id)
    else:    
        form=ReviewForm()
        return render(request,"reviews/review_form.html",{'form':form})
    
