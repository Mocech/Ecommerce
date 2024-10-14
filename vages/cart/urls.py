from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path("summary", views.cart_summary, name="cart-summary"),          # Cart summary - no product_id needed
    path("add/<int:product_id>/", views.cart_add, name="cart-add"),    # Add to cart - needs product_id
    path("delete/<int:product_id>/", views.cart_delete, name="cart-delete"), # Delete from cart - needs product_id
    path("update/<int:product_id>/", views.cart_update, name="cart-update"), # Update cart - needs product_id
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path("create_paypal_payment/", views.create_paypal_payment, name="create_paypal_payment"),
    path("execute_paypal_payment/", views.execute_paypal_payment, name="execute_paypal_payment"),

]
