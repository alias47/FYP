from django.shortcuts import render, redirect

from .models import Category, Photo
# Create your views here.


def buyPage(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()

    context = {'categories': categories, 'photos': photos}
    return render(request, 'buy.html', context)


def detailPage(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'detail.html', {'photo': photo})


def addPage(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        photo = Photo.objects.create(

            description=data['description'],
            image=image,
        )

        return redirect('buy')

    context = {'categories': categories}
    return render(request, 'add.html', context)
