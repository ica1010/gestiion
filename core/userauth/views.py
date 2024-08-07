from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from userauth.form import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login , authenticate, logout
from userauth.models import AdminProfile, SupplierProfile, User
from django.contrib.auth import update_session_auth_hash

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
    if not User.objects.filter(username='adminco').exists():
        # Créer un nouvel utilisateur 'admin' avec tous les privilèges d'administrateur
        User.objects.create_superuser(username='adminco', email='a.a.com', password='12345678')
        print("L'utilisateur 'admin' a été créé avec des privilèges d'administrateur.")
    else:
        print("L'utilisateur 'admin' existe déjà.")
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('homePage')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    profile = SupplierProfile.objects.get(user=user)
                    
                except SupplierProfile.DoesNotExist:
                    try:
                        profile = AdminProfile.objects.get(user=user)
                    except:
                        AdminProfile.objects.create(user=user)
                        profile = AdminProfile.objects.get(user=user)

                if not profile.active:
                    return HttpResponse('Your account was disabled')
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

def Profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST['email']
        phone=request.POST['phone']
        first = request.POST['first']
        last = request.POST['last']
        image = request.FILES.get('main-image')
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']

        user = User.objects.get(id = request.user.id)
        user.username = username
        user.email = email
        user.phone = phone
        user.first_name = first
        user.last_name = last
        if image:
            user.image=image
        if new_password :
            if not user.check_password(current_password):
                messages.error(request, 'Your current password is incorrect.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Important, to update the session with the new password
                messages.success(request, 'Your password was successfully updated!')
                return redirect('homePage')
        user.save()
        messages.success(request, f'your profile was update successfully')
        return redirect ('homePage')


    return render(request,'registration/profile.html')