# context_processors.py
def cart_processor(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())  # Calculate the total number of items in the cart
    return {
        'cart': cart,
        'total_items': total_items,
    }
