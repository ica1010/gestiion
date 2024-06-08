from django.conf import settings
from django.shortcuts import redirect, render
from userauth.form import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login , authenticate, logout
from userauth.models import User


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
        
            messages.success(request, f'Wellcome {username}, your account was successfully created')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    phone=form.cleaned_data['phone']
            )
            login(request , new_user)
            return redirect('homePage')
        
    else:
        form = UserRegisterForm()

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        messages.warning(request, f'you are already logged in.')
        return redirect('homePage')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username , password=password)

            if user is not None:
                login(request,user)
                messages.success(request, 'you are logged in .')
                return redirect ('homePage')
            else:
                messages.warning(request, 'user Does not exist , create an account.')
        except:
            messages.error(request, f'user with username : \'{username}\' does not exist')

    return render(request , 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'you are now logged out ')
    return redirect('sign-in')