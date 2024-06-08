
from gestion.models import Category, Product
from userauth.models import AdminProfile
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import now

def is_admin(user):
    try:
        admin_profile = AdminProfile.objects.get(user=user)
        return True
    except AdminProfile.DoesNotExist:
        return False
    
def default(request):
    admin = is_admin(request.user)
    filter_option = request.GET.get('filter', 'today')
    today = timezone.now().date()
    if filter_option == 'today':
        start_date = today
    elif filter_option == 'yesterday':
        start_date = today - timedelta(days=1)
    elif filter_option == 'last_7_days':
        start_date = today - timedelta(days=7)
    elif filter_option == 'last_30_days':
        start_date = today - timedelta(days=30)
    elif filter_option == 'this_month':
        start_date = today.replace(day=1)
    elif filter_option == 'last_month':
        first_day_of_current_month = today.replace(day=1)
        start_date = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
    else:
        start_date = today
    
    products_all = Product.objects.filter(created_at__gte=start_date)
    product_all_count = products_all.count()

    categories_all = Category.objects.all()
 
    return {
        'admin':admin,
        'products_all':products_all,
        'product_all_count':product_all_count,
        'filter_option':filter_option,
        'categories_all':categories_all,
    }
