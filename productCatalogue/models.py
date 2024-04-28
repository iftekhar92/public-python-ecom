from django.db import models
from django.utils.text import slugify
from categoryMgt.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    is_new = models.BooleanField()
    is_featured = models.BooleanField()
    short_description = models.TextField(default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to='uploads/products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)
    