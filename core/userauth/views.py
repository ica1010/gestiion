from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from userauth.form import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login , authenticate, logout
from userauth.models import AdminProfile, SupplierProfile, User


def add_user(request):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        admin = request.POST.get('admin')

        if not (username and phone and email):
            messages.error(request, "Please fill out all required fields.")
            return redirect(reverse('sign-up'))

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return redirect(reverse('sign-up'))

        new_user = User.objects.create_user(username=username, email=email, password='12345678')
        new_user.phone = phone
        new_user.save()

        if admin:
            AdminProfile.objects.create(user=new_user)
            messages.success(request, f"The admin user {username} was added successfully.")
        else:
            SupplierProfile.objects.create(user=new_user)
            messages.success(request, f"The supplier user {username} was added successfully.")

        return redirect(url)

    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse('sign-up'))
    

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are already logged in.')
        return redirect('homePage')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in.')
                return redirect('homePage')
            else:
                messages.warning(request, 'Invalid username or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, f'User with username \'{username}\' does not exist.')

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'you are now logged out ')
    return redirect('sign-in')