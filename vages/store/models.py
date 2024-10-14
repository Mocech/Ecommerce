from django.db import models
from djmoney.models.fields import MoneyField 

class Category(models.Model):
    
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency = 'KES', default=0)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='Product/',default='default.gif')
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    # category =models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
    #on sale
    on_sale = models.BooleanField(default=False)
    sale_price = MoneyField(max_digits=10, decimal_places=2, default_currency = 'KES', default=0)
    
    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    images = models.ImageField(upload_to= 'Product_Detail/images/')    
    alt_text = models.CharField(max_length=255, blank=True,null=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
class Offer(models.Model):    
    season =models.CharField(max_length=100)
    offer_discription = models.TextField()
    attractive_text = models.TextField()
    
    
    def __str__(self):
        return self.season
    
    
    
    
    
    