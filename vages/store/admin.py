from django.contrib import admin
from .models import Category,Product,Offer ,ProductImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Offer)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    
class ProductAdmin(admin.ModelAdmin):
    inlines =[ProductImageInline]
    
admin.site.register(ProductImage)    
    