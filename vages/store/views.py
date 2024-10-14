from django.shortcuts import render,get_object_or_404
from .models import Product,Offer
from django.views.generic.detail import DetailView


def home(request):
    trending_product = Product.objects.filter(on_sale=True)
    offer = Offer.objects.all()
    
    context ={
        'trending':trending_product,
        'Prod_offer':offer,
    }
    
    return render(request, 'app1/home.html', context)
class ProductDetail(DetailView):
    model = Product
    template_name = 'app1/product-details.html'
    context_object_name = 'product'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        context['images'] = self.object.images.all()
        return context

def about(request):
    return render(request, 'app1/about.html', {})

def blogs(request):
    return render(request, 'app1/blogs.html', {})

def contact(request):
    return render(request, 'app1/contact.html', {})

def shop(request):
      products = Product.objects.all()
    
      return render(request, 'app1/shop.html', {'product':products})

def review(request):
    return render(request, 'app1/review.html', {})
