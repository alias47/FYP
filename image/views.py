from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Photo, Myrating
from pprint import pprint
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .form import Photo
from django.db.models import Case, When
import pandas as pd
import requests
from django.core.paginator import Paginator
from django.contrib.auth.models import AnonymousUser
from image.form import edit
from django.contrib.auth.models import User
# Create your views here.


# LIST OF PROPERTY

def buyPage(request):
    
    categories = Category.objects.all()
    
    # photos = Photo.objects.filter(category__name=category)
    if 'q' in request.GET:
        q = request.GET['q']
        photos = Photo.objects.filter(location__icontains=q).order_by('-id')

    else:
        photos = Photo.objects.all().order_by('-id')
    
    
    photo_paginator = Paginator(photos, 6)
    page_num = request.GET.get("page")
    page = photo_paginator.get_page(page_num)

    context = {'photos': photos, 'categories': categories, 'page': page}
    return render(request, 'buy.html', context)


@login_required(login_url='login')
def detailPage(request, pk):

    photo = Photo.objects.get(id=pk)
    my_rating = 0

    try:
        myrating = Myrating.objects.get(photo=photo, user=request.user)
    except Myrating.DoesNotExist:
        myrating = None

    if myrating:
        my_rating = myrating.rating

    related_product = Photo.objects.filter(
        category=photo.category).exclude(id=pk)[:4]

    return render(request, 'detail.html',  {'photo': photo, 'related': related_product, 'my_rating': my_rating})


@login_required(login_url='login')
def rating(request, pk):
    # return HttpResponse(pk)

    photo = Photo.objects.get(id=pk)

    # For Rating
    if request.method == "POST":
        rate = request.POST['rating']
        if Myrating.objects.all().values().filter(photo_id=pk, user=request.user):
            Myrating.objects.all().values().filter(
                photo_id=pk, user=request.user).update(rating=rate)
        else:
            q = Myrating(user=request.user, photo=photo, rating=rate)
            q.save()

        # rate = request.POST['rating']
        # myrating = Myrating.objects.filter(photo_id=pk, user=request.user)

        # if myrating:
        #     myrating.update(rating=rate)
        # else:
        #     q = Myrating(user=request.user, photo=photo, rating=rate)
        #     q.save()

            messages.success(request, "Thank you for the rating")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    context = {'photo': photo}

    return render(request, '', context)


# FOR ADDING PROPERTY

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

# CATEGORY FUNCTION


def category(request, slug):
    category = Category.objects.get(slug=slug)

    photos = Photo.objects.filter(category=category)
    categories = Category.objects.all()

    # return HttpResponse(photos)
    return render(request, 'category.html', {'photos': photos, 'categories': categories})


# RECOMMENDATION

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

    context = {'property_list': property_list, 'categories': categories}

    return render(request, "recommendation.html", context)

 # FOR DELETING PROPERTY


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


# FOR EDITING PROPERTY

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
        photo.phone = request.POST["phone"]
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            photo.image = img
        photo.save()
        context["status"] = "Changes Saved Successfully"
    context["id"] = pid

    return render(request, 'editproduct.html', context)
