from django.urls import path
from . import views
from store.views import ProductDetail

app_name ='store'

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('blogs/',views.blogs,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('shop/',views.shop,name='shop'),
    path('review/',views.review,name='review'),
    path('product/<int:pk>/',ProductDetail.as_view(),name='product'), 
]
