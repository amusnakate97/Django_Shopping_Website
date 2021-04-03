from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home,name='e_commerce-home'),
path('shop/', views.showHome,name='shop'),
path('logout/', views.logOutUser,name='logout'),
path('register/', views.register,name='e_commerce-register'),
path('shop/showItems/(?P<gender>\s+)/$',views.showProducts,name='e-products'),
url(r'^shop/(?P<id>\d+)/$',views.addToCart,name='add'),
url(r'^shop/delete/(?P<id>\d+)/$',views.deleteItemFromCart,name='remove'),
url(r'^shop/update/(?P<id>\d+)/$',views.updateItemFromCart,name='update'),
path('bill/', views.generateBill,name='bill'),
path('filter/', views.filter, name='filter'),
path('saveHistory/', views.savePastOrder, name='savePastOrders'),
path('reviewOrder/', views.OrderReview, name='review'),
path('profile/', views.profileSetUp,name="profile"),
path('^shop/get_review/(?P<id>\d+)/$', views.productReview,name="get_review"),
path('^shop/get_details/(?P<id>\d+)/$', views.productDetails,name="get_details"),


#url(r'^shop/update/(?P<id>\d+)/$',views.updateItemFromCart,name='update'),

path("shop/showCart/",views.showCart,name='cart')]
