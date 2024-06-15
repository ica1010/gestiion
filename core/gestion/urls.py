from django.urls import include, path
from . views import *



urlpatterns = [
    path('',HomePage, name='homePage'),

    ############################## authentifications urls ############################
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('userauth.urls')),

    ################################### article urls ##################################

    path('add-article/',Add_article, name='add_article'),
    path('articles-list/',Article_list, name='article_list'),
    path('articles-detail/<pid>',Article_detail, name='article_detail'),
    path('edit-articles/<pid>',Edit_article, name='edit_article'),
    path('delete-articles/<pid>',Remove_article, name='remove_article'),

    ################################### fournisseur urls ##################################

    path('fournisseur/',Four_list, name='fourn'),
    path('fournisseur/add/',add_fourn, name='add_fourn'),
    path('fournisseur/<fid>',delete_fourn, name='delete_fourn'),
    path('fournisseur/update/<fid>',update_fourn, name='update_fourn'),



    ################################### services urls ##################################

    path('services/',Serv_list, name='serv'),
    path('services/add/',add_serv, name='add_serv'),
    path('services/<sid>',delete_serv, name='delete_serv'),
    path('services/update/<sid>',update_serv, name='update_serv'),

    ################################### article category urls ##################################

    path('articles-categories/',Article_catgoies, name='article_catgoies'),
    path('add-new-category/',Add_category, name='add_category'),
    path('delete-category/<cid>' ,Remove_category, name='delete_category'),
    path('edit-category/<cid>' ,Edit_category, name='edit_category'),

    ################################### users urls ###########################################
    path('search/',search_view ,name='search'),
    path('suppliers/' ,Suppliers, name='suppliers'),
    path('deletes-user/<id>' ,Del_supplier, name='delete_user'),
    path('toggle-supplier-status/', toggle_supplier_status, name='toggle_supplier_status'),
    ################################## deliveries urls #######################################

    path('deliveries/' ,Deliveries, name='deliveries'),
    path('add-delivery/' ,Add_Delivery, name='add_delivery'),
    path('delivery-detail/<did>' ,DeliveryDetail, name='delivery'),

    ################################### supplies urls #######################################
    path('supplies/' ,Supply_view, name='supplies'),
    path('supplies-detail/<sid>' ,SupplyDetail, name='supplies-detail'),
    path('add-supply/' ,Add_supply, name='Add_supply'),

    ################################### reports urls #######################################
    path('reports/' ,reports, name='reports'),



]
