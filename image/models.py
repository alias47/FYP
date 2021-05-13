from django.db import models
from django.contrib.auth.models import User, Permission

from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

# class Category(models.Model):

#     name = models.CharField(max_length = 100, null = False, blank = False)

#     def __str__(self):
#         return self.name


class Photo(models.Model):
    # category = models.ForeignKey(Category , on_delete= models.SET_NULL, null=True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    price = models.IntegerField()
    bed = models.IntegerField(default=4)
    phone = models.IntegerField(default=1426874)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.description + ' | ' + str(self.author)
        return self.location
        return self.price
        return self.bed
        return self.phone
      


class Myrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):

        return str(self.rating)
        