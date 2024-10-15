$(document).ready(function() {
    // Handle delete button clicks
    $('.btn-remove').click(function(event) {
        event.preventDefault();
        var dataUrl = $(this).data('url'); // Store the data-url in a variable
        console.log('Data URL:', dataUrl); // Log the data-url for debugging
    
        var productId = dataUrl.split('/').filter(Boolean).pop(); // Extract product_id from data-url
    
        // Log the extracted Product ID
        console.log('Extracted Product ID:', productId); // Log the product ID for debugging
    
        // Ensure productId is not empty
        if (!productId) {
            console.error('Product ID is empty. Cannot delete the item.');
            return; // Exit if product ID is not valid
        }
    
        console.log('Deleting item with ID:', productId); // Log the product ID for debugging
        $.ajax({
            type: 'POST',
            url: dataUrl + '?_=' + new Date().getTime(), // Add cache-busting parameter
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                console.log('Response from server:', response); // Log the response for debugging
                if (response.status === 'success') {
                    $('#cart-item-' + productId).remove(); // Remove item from UI
                    console.log('Item removed from UI'); // Log removal
                    updateCartSummary(); // Update the summary after deletion
                    console.log('Updating cart summary'); // Log summary update
                } else {
                    alert(response.message); // Alert the error message
                }
            }
        });
    });
    
      
      function updateCartSummary() {
        let totalQuantity = 0;
        let totalPrice = 0;
    
        $('.current_quantity').each(function() {
            const quantity = parseInt($(this).text()) || 0; // Default to 0 if parsing fails
            
            // Use closest to find the parent, then find the child with class "get_p"
            const priceElement = $(this).closest('.quantity-text').find('.get_p');
            
            // Log the price element to check if it’s selected correctly
            console.log('Price Element:', priceElement); // Log the price element
            console.log('Current HTML of Price Element:', priceElement[0]); // Log the actual HTML element
    
            // Get the data-price attribute and parse it
            const priceAttr = priceElement.attr('data-price');
            console.log('Data-price attribute:', priceAttr); // Log data-price for debugging
    
            // Remove the currency symbol and convert to float
            const price = parseFloat(priceAttr.replace(/[^0-9.-]+/g,"")) || 0; // Regex to strip out non-numeric characters
            
            console.log('Current Quantity:', quantity, 'Price:', price); // Log quantity and price for debugging
    
            totalQuantity += quantity;
            totalPrice += quantity * price;
        });
    
        console.log('Total Quantity:', totalQuantity, 'Total Price:', totalPrice); // Log final totals for debugging
    
        $('#cart-total-price').text(totalPrice.toFixed(2)); // Update total price display
        $('.logo .span.logo').text(`(${totalQuantity})`); // Update total quantity in the logo
    }
    
});
