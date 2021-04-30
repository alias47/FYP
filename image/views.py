from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Photo
from pprint import pprint
from django.http import HttpResponse
# Create your views here.


def buyPage(request):
    
    photos = Photo.objects.filter(category__name=category)
    if 'q' in request.GET:        
        q=request.GET['q']
        photos = Photo.objects.filter(description__icontains=q)
        
    else:    
        photos = Photo.objects.all() 

    categories = Category.objects.all()

    context = {'photos':photos,'categories':categories}
    return render(request, 'buy.html', context)

# def buyPage(request):
#     category = request.GET.get('category')
#     if category == None:
#         photos = Photo.objects.all()
#     else:
#         photos = Photo.objects.filter(category__name=category)

#     categories = Category.objects.all()

#     context = {'categories': categories, 'photos': photos}
#     return render(request, 'buy.html', context)


def detailPage(request, pk):

    photo = Photo.objects.get(id=pk)
    related_product = Photo.objects.filter(category=photo.category)
    return render(request, 'detail.html', {'photo': photo, 'related':related_product})




@login_required(login_url='login')
def addPage(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(

            category=category,
            description=data['description'], location=data['location'], price=data['price'], bed=data['bed'], bathroom=data['bathroom'],
            image=image
        )

        return redirect('buy')

    context = {'categories': categories}
    return render(request, 'sell.html', context)


def category(request, slug):
    category=Category.objects.get(slug=slug)

    photos = Photo.objects.filter(category=category)
    
    categories = Category.objects.all()

    # return HttpResponse(photos)
    return render(request, 'category.html', {'photos': photos,'categories':categories})
