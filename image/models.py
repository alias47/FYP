from django.db import models

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
    image = models.ImageField(null=False, blank = False)
    description = models.TextField(blank=True, null=True)
    location = models.TextField()
    price = models.IntegerField()
    bed = models.IntegerField()
    bathroom = models.IntegerField()
    is_featured=models.BooleanField(default=False)


    def __str__(self):
        return self.description
        return self.location
        return self.price
        return self.bed
        return self.bathroom

