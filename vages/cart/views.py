import paypalrestsdk                             
import base64
import requests
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem,Payment
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt,csrf_protect,ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth.decorators import login_required

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Migrate session cart items to user cart if they exist
        session_key = request.session.session_key
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key).first()
            if session_cart:
                for item in session_cart.cartitem_set.all():
                    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=item.product)
                    cart_item.quantity += item.quantity  # Adjust quantity if necessary
                    cart_item.save()
                session_cart.delete()  # Clear session-based cart after migration
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    return cart


@csrf_protect
def cart_add(request, product_id):
    # Fetch the product using the product_id
    product = get_object_or_404(Product, id=product_id)

    # Get the quantity from the request data
    quantity = int(request.POST.get('quantity', 1))

    # Check if user is authenticated or handle session-based cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Add or update the product in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # Update the quantity with the submitted quantity
    cart_item.quantity = quantity
    cart_item.save()
    
    messages.success(request, f'Product has successfully added to cart.') 

    # Respond with a success message
    return JsonResponse({'status': 'success', 'message': f"Added {quantity} {product.name}"})


def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity < 1:
                return JsonResponse({'status': 'error', 'message': 'Quantity must be at least 1.'})

            # Get the correct cart based on authentication status
            cart = get_cart(request)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.quantity = quantity
            item.save()
             
            messages.success(request, f'The quantity of {item.product.name} has been updated successfully.') 
            # Calculate new totals
            total_item_price = item.product.price * item.quantity
            total_price, total_quantity = calculate_cart_totals(cart)

            return JsonResponse({
                'status': 'success',
                'total_item_price': float(total_item_price.amount),
                'cart_total': float(total_price.amount),
                'total_quantity': total_quantity
            })

        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid quantity.'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    print("Invalid request method.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



@csrf_exempt
def cart_delete(request, product_id):
    if request.method == 'POST':
        # Retrieve the appropriate cart for the current user or session
        cart = get_cart(request)
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if item:
            item.delete()  # Remove the item from the cart
            messages.success(request, f'{item.product.name} has been removed from your cart.')
            # Recalculate totals for the updated cart
            total_price, total_quantity = calculate_cart_totals(cart)

            return JsonResponse({
                'status': 'success',
                'message': 'Item removed successfully.',
                'total_price': float(total_price.amount),
                'total_quantity': total_quantity
            })
        
        return JsonResponse({'status': 'error', 'message': 'Item not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

def calculate_cart_totals(cart):
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.product.price for item in items)
    total_quantity = sum(item.quantity for item in items)
    return total_price, total_quantity
def cart_summary(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price of all items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)
    
    # Calculate the total quantity of all items in the cart
    total_quantity = sum(item.quantity for item in cart_items)
    
    return render(request, 'cart/cart_summary.html', {
        'aggregated_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity  # This will give you the sum of all quantities
    })
@ensure_csrf_cookie
def checkout(request):
    print("Checkout view executed")  # Debug: View execution confirmation

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated.'})

    try:
        # Retrieve the user's cart
        cart = Cart.objects.get(user=request.user)
        print("Cart found:", cart)  # Debug: Cart found
    except Cart.DoesNotExist:
        print("No cart found for user.")  # Debug: Cart not found
        return JsonResponse({'status': 'error', 'message': 'Cart not found.'})

    # Attempt to retrieve cart items
    cart_items = cart.cartitem_set.all()  # Use this line if you haven't defined related_name
    # Uncomment the next line if you have defined related_name='cart_items' in CartItem model
    # cart_items = cart.cart_items.all()  

    if not cart_items:
        print("No items in cart.")  # Debug: Cart is empty
    else:
        for item in cart_items:
            # Debug: Print item details
            print("Item:", item.product.name,  # Assuming you have a name field in Product model
                  "Price:", item.product.price,
                  "Quantity:", item.quantity,
                  "Total:", item.get_total_price())

    # Calculate the total price of the cart items
    total_price = sum(item.get_total_price() for item in cart_items)
    print("Debug Total Price:", total_price)  # Debug: Total price calculation

    # Prepare the context for rendering the checkout template
    context = {
        'total_price': total_price,
        'show_nav':False,
        'show_footer':False
    }
    
    return render(request, 'cart/checkout.html', context)

@csrf_protect  # Use CSRF protection
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        # Validate input
        if not phone_number or not amount:
            return JsonResponse({'status': 'error', 'message': 'Phone number and amount are required.'})

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid amount.'})

            # Prepare for STK Push
        api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {get_access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "LipaNaMpesaOnline": "lipa-na-mpesa-online",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.CALLBACK_URL,
            "AccountReference": "YourAccountReference",
            "TransactionDesc": "Payment for Order"
        }

        # Debug: Log the payload
        print("Payload for payment initiation:", payload)

        response = requests.post(api_url, json=payload, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            # Save payment details to the database
            payment = Payment.objects.create(
                phone_number=phone_number,
                amount=amount,
                cart=Cart.objects.get(user=request.user),  # Assuming the user is logged in
                status='pending'
            )
            return JsonResponse({'status': 'success', 'message': 'Payment initiated!'})
        else:
            return JsonResponse({'status': 'error', 'message': response_json.get('errorMessage', 'Payment initiation failed.')})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

def get_access_token():
    api_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(api_url, headers=headers)

    # Debug: Log the response status code and text
    print("Response Status Code:", response.status_code)  # Debug: Check the status code
    print("Response Text:", response.text)  # Debug: Check the response text

    try:
        json_response = response.json()
        return json_response['access_token']
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response.")  # Debug: Handle JSON decode error
        return None  # Return None or raise an exception

@csrf_protect  # Use CSRF protection
def payment_callback(request):
    if request.method == 'POST':
        # Handle the callback data
        data = request.body.decode('utf-8')
        # Parse the incoming data and update the payment status in your database

        return JsonResponse({'status': 'received'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

# Initialize the PayPal SDK with credentials
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" in production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})


def create_paypal_payment(request):
    # Debugging: Log the request method
    print(f"Request method: {request.method}")
    
    if request.method == "POST":
        cart_id = request.session.get('cart_id')
        if not cart_id:
            return JsonResponse({"error": "Cart not found."}, status=400)

        cart = Cart.objects.get(id=cart_id)
        total_price, _ = calculate_cart_totals(cart)

        # Convert total_price to string and format it correctly
        total_price_str = "{:.2f}".format(total_price)  # Ensure two decimal places

        # Create a PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/execute/'),
                "cancel_url": request.build_absolute_uri('/checkout/'),
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Your Order",
                        "sku": "order",
                        "price": total_price_str,  # Use the formatted price
                        "currency": "KES",  # Set currency to KES
                        "quantity": 1
                    }]
                },
                "amount": {"total": total_price_str, "currency": "KES"},  # Use KES for amount
                "description": "Payment for order",
            }]
        })

        # Debugging: Log payment creation result
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    # Redirect to PayPal for approval
                    return JsonResponse({"approval_url": link.href})
        else:
            print(f"Payment error: {payment.error}")
            return JsonResponse({"error": "Error creating PayPal payment."}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)

def execute_paypal_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return redirect("store:home")  # Success redirect
    else:
        print(payment.error)
        return redirect("checkout")  # Error redirect
    
    
