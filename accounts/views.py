
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm,ProfileForms

def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form=ProfileForms(request.POST,request.FILES)
        if user_form.is_valid():
            user=user_form.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('show_blogs')
    else:
        user_form = SignUpForm()
        profile_form=ProfileForms()
    return render(request, 'registration/signup.html', {'user_form': user_form,'profile_form':profile_form})
    
    
def show_profile(request):
    return render(request, 'profile.html')