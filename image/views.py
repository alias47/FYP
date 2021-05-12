from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Photo, Myrating
from pprint import pprint
from django.http import HttpResponse, Http404
from django.contrib import messages
from .form import Photo
from django.db.models import Case, When
import pandas as pd
import requests
from django.http import HttpResponseRedirect
from image.form import edit
from django.contrib.auth.models import User
# Create your views here.

# buying page


def buyPage(request):

    # photos = Photo.objects.filter(category__name=category)
    if 'q' in request.GET:
        q = request.GET['q']
        photos = Photo.objects.filter(location__icontains=q).order_by('-id')

    else:
        photos = Photo.objects.all().order_by('-id')

    categories = Category.objects.all()

    context = {'photos': photos, 'categories': categories}
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

# property detail


def detailPage(request, pk):

    photo = Photo.objects.get(id=pk)
    related_product = Photo.objects.filter(category=photo.category).exclude(id=pk)[:4]
    return render(request, 'detail.html', {'photo': photo, 'related': related_product})

# for adding property


@login_required(login_url='login')
def addPage(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        author = request.user

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            author=author,
            category=category,
            description=data['description'], location=data['location'], price=data['price'], bed=data['bed'], phone=data['phone'],
            image=image
        )

        return redirect('buy')

    context = {'categories': categories}
    return render(request, 'sell.html', context)

# category function


def category(request, slug):
    category = Category.objects.get(slug=slug)

    photos = Photo.objects.filter(category=category)

    categories = Category.objects.all()

    # return HttpResponse(photos)
    return render(request, 'category.html', {'photos': photos, 'categories': categories})


@login_required(login_url='login')
def rating(request, pk):
    # return HttpResponse(pk)

    photos = get_object_or_404(Photo, id=pk)
    photo = Photo.objects.get(id=pk)

    # For Rating
    if request.method == "POST":
        rate = request.POST['rating']
        myrating = Myrating.objects.filter(photo_id=pk, user=request.user)
       
        if myrating:
            myrating.update(rating=rate)
        else:
            q = Myrating(user=request.user, photo=photo, rating=rate)
            q.save()

        messages.success(request, "Rating has been submitted!")

    # displaying rating in detail page
    photo_rating = 0
    rate_flag = False

    context = {'photo': photo, 'photo_rating': photo_rating,
               'rate_flag': rate_flag}
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return render(request, 'ratings.html',context)


def similar(property_location, rating, corrMatrix):
    similar_ratings = corrMatrix[property_location]*(rating-3)
    return similar_ratings

@login_required(login_url='login')
def collaborative(request):
    categories = Category.objects.all()
    property_rating = pd.DataFrame(list(Myrating.objects.all().values()))

    new_user = property_rating.user_id.unique().shape[0]

    active_user = request.user.id

    # no user has rated any property

    if active_user > new_user:
        photo = Photo.objects.get(id=5)
        q = Myrating(user=request.user, photo=photo, rating=0)
        q.save()

    userRatings = property_rating.pivot_table(
        index=['user_id'], columns=['photo_id'], values='rating')
    userRatings = userRatings.fillna(0, axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(Myrating.objects.filter(
        user=request.user).values())).drop(['user_id', 'id'], axis=1)
    user_filtered = [tuple(x) for x in user.values]
    photo_id_watched = [each[0] for each in user_filtered]

    similar_property = pd.DataFrame()
    for photo, rating in user_filtered:
        similar_property = similar_property.append(similar(
            photo, rating, corrMatrix), ignore_index=True)

    photo_id = list(similar_property.sum().sort_values(ascending=False).index)
    photo_id_recommend = [
        each for each in photo_id if each not in photo_id_watched]
    preserved = Case(*[When(pk=pk, then=pos)
                       for pos, pk in enumerate(photo_id_recommend)])
    property_list = list(Photo.objects.filter(
        id__in=photo_id_recommend).order_by(preserved)[:9])

    context = {'property_list': property_list, 'categories':categories}

    return render(request, "recommendation.html", context)


 # for deleting property
@login_required(login_url='login')
def deletePage(request, pk):
    context = {}
    pid = pk

    photo = get_object_or_404(Photo, id=pid)
    context["photo"] = photo


    if request.method == "POST":
        photo.delete()
        context["status"] = str(photo.location)+" removed Successfully!!!"
        return redirect("buy")
    else:
        return render(request, "delete.html", context)

# for editing property

@login_required(login_url='login')
def edit(request, pk):
    context = {}
    pid = pk
    photo = get_object_or_404(Photo, id=pid)
    context["photo"] = photo
    if request.method == 'POST':
        photo.price = request.POST["pp"]
        photo.description = request.POST["des"]
        photo.bed = request.POST["bed"]
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            photo.image = img
        photo.save()
        context["status"] = "Changes Saved Successfully"
    context["id"] = pid

    return render(request, 'editproduct.html', context)
