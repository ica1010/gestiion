
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout,authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required , permission_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.urls import reverse
from . models import *
# from userauth.form import UserRegisterForm
from userauth.models import SupplierProfile , User
# Create your views here.
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import now
from django.db import transaction
from django.utils.dateparse import parse_date


def is_admin(user):
    try:
        admin_profile = AdminProfile.objects.get(user=user)
        return True
    except AdminProfile.DoesNotExist:
        return False

@login_required(login_url='sign-in')
def HomePage(request):
    admin = False
    suppliers = SupplierProfile.objects.all()
    actions = Action.objects.all()

    admin = is_admin(request.user)
    if admin :
        products = Product.objects.all()
        deliveries = Delivery.objects.all()
        supplies = Supply.objects.all()
    else:
        products = Product.objects.all()
        deliveries = Delivery.objects.filter(user = request.user)
        supplies = Supply.objects.filter(user = request.user)

    product_count = products.count()
    deliveries_count = deliveries.count()
    supplies_count = supplies.count()
    suppliers_count = suppliers.count()

    context={
        'actions':actions,
        'products':products,
        'product_count':product_count,
        'deliveries_count':deliveries_count,
        'supplies_count':supplies_count,
        'suppliers_count':suppliers_count,
        'admin':admin,
    }
    return render(request, 'pages/homePage.html', context)

######################################################## article views #################################################################################################
def Add_article(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        code = request.POST['code']
        title = request.POST['title']
        description = request.POST['description']
        stock = request.POST['stock']
        category = request.POST['category']
        # short_description = request.POST['short-description']
        image = request.FILES.get('main-image')

        category = Category.objects.get(
            title=category
        )
        new_article = Product.objects.create(
            title = title,
            category = category,
            quantity = stock,
            description = description,
        )
        if code :
            new_article.pid = code

        if image :
            new_article.image = image

        new_article.save()
        new_action = Action.objects.create(
            user = request.user,
            action = new_article    
        )
        messages.success(request, 'the product was added successfully')
        return redirect('article_list')

    context = {
        'categories':categories,
    }
    return render(request, 'pages/article/add_article.html',context)

def Article_list(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    products = Product.objects.all().order_by('quantity')
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            products = products.filter(created_at__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            products = products.filter(created_at__lte=end_date)
    categories = Category.objects.all()
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = paged_products.count(value=products)

    context = {
        'products' :products ,
        'categories' :categories ,
        'paged_products':paged_products,
        'product_count':product_count,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,
    }
    return render(request, 'pages/article/article_list.html', context )

def Article_detail(request, pid):
    product = Product.objects.get(pid = pid)

    context = {
        'product' :product
    }
    return render(request, 'pages/article/article_detail.html', context )

def Edit_article(request, pid):
    product = Product.objects.get(pid=pid)
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        stock = request.POST['stock']
        cat = request.POST['category']
        image = request.FILES.get('main-image')

        category = Category.objects.get(title=cat)

        product = Product.objects.get(pid = pid)
        product.title = title
        product.category = category
        product.quantity = int(stock)
        product.description = description
        
        if image :
            product.image = image
        product.save()
        messages.success(request, f'the product {product.title} was update successfully')
        return redirect('article_list')


    context = {
        'product' :product,
        'categories':categories
    }

    return render(request, 'pages/article/edit_article.html', context )

def Remove_article(request, pid):

    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(
        pid = pid
    )
    product.delete()
    return redirect(url)

######################################################## article categories views #################################################################################################

def Article_catgoies(request):
    categories = Category.objects.all()

    context = {
        'categories':categories,
    }
    return render(request, 'pages/article/article_category.html', context)

def Add_category(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        title = request.POST['title']
    category = Category.objects.create(
        title = title
    )
    category.save()
    return redirect(url)

def Edit_category(request, cid):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        title = request.POST['title']
    category = Category.objects.get(cid = cid)
    category.title = title
    category.save()
    return redirect(url)

def Remove_category(request, cid):

    url = request.META.get('HTTP_REFERER')
    category = Category.objects.get(
        cid = cid
    )
    category.delete()
    return redirect(url)

######################################################## Search views #################################################################################################

def search_view(request):
    query = request.GET.get('q')
    products = None
    url = request.META.get('HTTP_REFERER')

    products = Product.objects.filter(Q(title__icontains=query))
    category = Category.objects.filter(Q(title__icontains=query))

    context = {
        'products': products,
        'category': category,
        'query': query,
    }
    if query:
        return render(request, 'pages/search/search_all.html', context)
    else:
        return redirect (url)


######################################################## Suppliers & Delivers views #################################################################################################
def toggle_supplier_status(request):
    user_id = request.POST.get('user_id')
    if user_id:
        try:
            user_profile = get_object_or_404(SupplierProfile, user__id=user_id)
        except:
            user_profile = get_object_or_404(AdminProfile, user__id=user_id)

        user_profile.active = not user_profile.active
        user_profile.save()


    return HttpResponseRedirect(reverse('suppliers'))  # Redirect to the suppliers page

def Suppliers(request):
    user_id = request.GET.get('user_id')
    suppliers = SupplierProfile.objects.all()

    if user_id :
        user_profile = SupplierProfile.objects.get(user__id = user_id)
        user_profile.active != user_profile.active
    admin = AdminProfile.objects.all()
    all_user = list(admin)+list(suppliers)
    context = {
        'all_user':all_user,
        'admin':admin,
    }
    return render(request, 'pages/users/suppliers.html', context)

def Del_supplier(request, id):
    try:
        person = get_object_or_404(AdminProfile, user__id=id)
    except:
        person = get_object_or_404(SupplierProfile, user__id=id)

    if person.user.id == request.user.id :
        pass
    else:
        person.delete()
    if is_admin(User.objects.get(username = person)):
        messages.success(request, "L'administrateur a été supprimé avec succès.")
    else:
        messages.success(request, "Le fournisseur a été supprimé avec succès.")

    return redirect(reverse('suppliers'))

def Supply_view(request):
    products = Product.objects.all()
    fournisseurs = Fournisseur.objects.all()
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')

    admin = is_admin(request.user)
    if admin :
        supplies = Supply.objects.all().order_by('-date')

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                supplies = supplies.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                supplies = supplies.filter(date__lte=end_date)


    else :
        supplies = Supply.objects.filter(user = request.user).order_by('-date')
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                supplies = supplies.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                supplies = supplies.filter(date__lte=end_date)
                
    context = {
        'supplies':supplies,
        'products':products,
        'fournisseurs':fournisseurs,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,
    }
    return render(request, 'pages/supplies/supplies.html', context)

def Deliveries(request) :
    products = Product.objects.all()
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    admin = False
    admin = is_admin(request.user)
    if admin :
        deliveries = Delivery.objects.all()
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                deliveries = deliveries.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                deliveries = deliveries.filter(date__lte=end_date)
    else:
        deliveries = Delivery.objects.filter(user=request.user)
    services = Service.objects.all()
    deliveries_product = DeliveryProduct.objects.all()

    context = {
        'deliveries':deliveries,
        'products':products,
        'services':services,
        'deliveries_product': deliveries_product,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,
    }
    return render(request, 'pages/deliveries/deliveries.html', context)

def Add_Delivery(request):
    url = request.META.get('HTTP_REFERER')
    products = []
    quantities = []
    if request.method == 'POST':
        products = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        service = request.POST.get('service')
        post = request.POST.get('post')
        code = request.POST.get('code')

    newDelivery = Delivery.objects.create(
        user = request.user,
        post = post,
        service = service
    )
    if code :
        newDelivery.did = code

        newDelivery.save()
    for product in products :
        product_e = Product.objects.get(title = product)
        product_e.quantity = product_e.quantity - int(quantities[products.index(product)])
        product_e.save()
        DeliveryProduct.objects.create(
            delivery = newDelivery,
            product = product_e,
            quantity = quantities[products.index(product)],
        )
    newDelivery.save()

    return redirect(url)

def Add_supply(request):
    url = request.META.get('HTTP_REFERER')
    products = []
    quantities = []
    livrer_name = []
    livrer_phone = []
    fournisseur = []
    detail = []
    code = []
    if request.method == 'POST':
        products = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        livrer_name = request.POST.getlist('livrer-name')
        livrer_phone = request.POST.getlist('livrer-phone')
        fournisseur = request.POST.getlist('fournisseur')
        detail = request.POST.getlist('detail')
        code = request.POST.getlist('code')

    for product in products :
        fournisseur_in = Fournisseur.objects.get(title = fournisseur[products.index(product)])
        product_e = Product.objects.get(title = product)
        product_e.quantity = product_e.quantity + int(quantities[products.index(product)])
        product_e.save()
        response = f'products = {products}, fourn = {fournisseur}, livre = {livrer_name}, phone = {livrer_phone}, detail = {detail}'
        try :
            new_supply  = Supply.objects.create(
                user = request.user,
                product = product_e,
                quantity = quantities[products.index(product)],
                fournisseur = fournisseur_in,
                livrer_name = livrer_name[products.index(product)],
                livrer_phone = livrer_phone[products.index(product)],
                detail = detail[products.index(product)],
            )
            if code[products.index(product)]:
                new_supply.sid = code[products.index(product)]
                new_supply.save()

            messages.success(request, f'la sortie a ete engistrer avec sucess')
        except Exception as e :
            messages.error(request, e)
            return url

    return redirect(url)


def DeliveryDetail(request, did) :
    delivery = Delivery.objects.get(did=did)
    products = DeliveryProduct.objects.filter(delivery=delivery.id)
    context = {
        'delivery':delivery,
        'products':products,
    }
    return render(request, 'pages/deliveries/delivery-detail.html', context)

def SupplyDetail(request, sid) :
    supply = Supply.objects.get(sid=sid)
    context = {
        'supply':supply,
    }
    return render(request, 'pages/supplies/supply-detail.html', context)

def Four_list(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    fournisseurs = Fournisseur.objects.all()
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            fournisseurs = fournisseurs.filter(date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            fournisseurs = fournisseurs.filter(date__lte=end_date)
    context={
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,
        'fournisseurs':fournisseurs,
    }
    return render(request, 'pages/article/fournisseur.html', context)


def Serv_list(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    services = Service.objects.all()
    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            services = services.filter(date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            services = services.filter(date__lte=end_date)
    context={
        'services':services,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,

    }
    return render(request, 'pages/article/service.html', context)

def delete_fourn(request, fid):
    url = request.META.get('HTTP_REFERER')
    fournisseur = Fournisseur.objects.get(fid=fid)
    message = f'le fournisseur {fournisseur.title} a ete supprimé avec succes'
    fournisseur.delete()
    messages.success(request , message)
    return redirect(url)


def delete_serv(request, sid):
    url = request.META.get('HTTP_REFERER')
    service = Service.objects.get(sid=sid)
    message = f'le service {service.title} a ete supprimé avec succes'
    service.delete()
    messages.success(request , message)
    return redirect(url)

def update_fourn(request, fid):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        new_tilte = request.POST.get('new_title')
        code = request.POST.get('code')
    fournisseur = Fournisseur.objects.get(fid=fid)

    try:
        if new_tilte :
            fournisseur.title=new_tilte
        if code:
            fournisseur.fid=code

        fournisseur.save()
        messages.success(request , 'modification fait avec success')
    except Exception as e :
        messages.success(request ,e)
    return redirect(url)


def update_fourn(request, fid):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        new_tilte = request.POST.get('new_title')
        code = request.POST.get('code')
    fournisseur = Fournisseur.objects.get(fid=fid)

    try:
        if new_tilte :
            fournisseur.title=new_tilte
        if code:
            fournisseur.fid=code

        fournisseur.save()
        messages.success(request , 'modification fait avec success')
    except Exception as e :
        messages.success(request ,e)
    return redirect(url)


def update_serv(request, sid):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        new_tilte = request.POST.get('new_title')
        code = request.POST.get('code')
    service = Service.objects.get(sid=sid)

    try:
        if new_tilte :
            service.title=new_tilte
        if code:
            service.sid=code

        service.save()
        messages.success(request , 'modification fait avec success')
    except Exception as e :
        messages.success(request ,e)
    return redirect(url)


def add_fourn(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        tilte = request.POST.get('title')
        code_fournisseur = request.POST.get('code')

    try:
        new_fourn = Fournisseur.objects.create(
            title = tilte
        )
        if code_fournisseur:
            new_fourn.fid = code_fournisseur

        new_fourn.save()
        messages.success(request , f'{new_fourn.title} , a été ajouté aux fournisseur avec succes')
        return redirect(url)

    except Exception as e :
        messages.success(request ,e)
        return redirect(url)


def add_serv(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        tilte = request.POST.get('title')
        code_serv = request.POST.get('code')

    try:
        new_serv = Service.objects.create(
            title = tilte
        )
        if code_serv:
            new_serv.sid = code_serv

        new_serv.save()
        messages.success(request , f'{new_serv.title} , a été ajouté aux services avec succes')
        return redirect(url)

    except Exception as e :
        messages.success(request ,e)
        return redirect(url)


def reports(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    products = Product.objects.all()
    supplies = Supply.objects.all()
    deliveries = Delivery.objects.all()

    if start_date:
        start_date = parse_date(start_date)
        if start_date:
            products = products.filter(created_at__gte=start_date)
            supplies = supplies.filter(date__gte=start_date)
            deliveries = deliveries.filter(date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        if end_date:
            products = products.filter(created_at__lte=end_date)
            supplies = supplies.filter(date__lte=end_date)
            deliveries = deliveries.filter(date__lte=end_date)

    deliveries_product = DeliveryProduct.objects.all()

    context = {
        'products': products,
        'supplies': supplies,
        'deliveries': deliveries,
        'deliveries_product': deliveries_product,
        'start_date': start_date,
        'end_date': end_date,
        'start_date_i': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date_i': end_date.strftime('%Y-%m-%d') if end_date else None,

    }

    return render(request, 'pages/report/reports.html', context)