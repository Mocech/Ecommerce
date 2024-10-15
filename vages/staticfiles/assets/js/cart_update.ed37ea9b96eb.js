$(document).ready(function() {
    $('.btn-quantity').on('click', function(event) {
        event.preventDefault();

        const isPlus = $(this).hasClass('plus');
        const isMinus = $(this).hasClass('minus');
        const itemId = $(this).closest('.item').attr('id').split('-')[2]; // Extract item ID correctly
        const url = $(this).data('url');

        const quantityElement = $(`#item-quantity-${itemId}`);
        let currentQuantity = parseInt(quantityElement.text());

        if (isPlus) {
            currentQuantity += 1;
        } else if (isMinus && currentQuantity > 1) {
            currentQuantity -= 1;
        } else {
            return; // Exit if quantity is invalid
        }

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                quantity: currentQuantity,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                console.log('Response from server:', response); // Log the response for debugging
                if (response.status === 'success') {
                    // Update the item's price in the UI based on the response
                    $('#item-quantity-' + itemId).text(currentQuantity); // Update the quantity displayed
                    $('#item-price-' + itemId).text(`KES${response.total_item_price.toFixed(2)}`); // Update the individual item price
                    updateCartSummary(response.cart_total, response.total_quantity); // Update the cart summary immediately

                    // ** New Code: Update the total price in the cart summary **
                    $('#cart-total-price').text(`KES${response.cart_total.toFixed(2)}`);
                } else {
                    alert(response.message); // Alert the error message
                }
            }
        });
    });
});

// Function to update the cart summary
function updateCartSummary(total, quantity) {
    $('#cart-total-price').text(`KES${total.toFixed(2)}`); // Update the cart total price
    $('.logo .span').text(`(${quantity})`); // Update the cart item count in the logo
}
