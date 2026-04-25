from django.db import models

class Artisan(models.Model):
    
    name = models.CharField(max_length=100)

    service = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    email = models.EmailField(default='example@example.com')
    experience = models.IntegerField()

    description = models.TextField()

    image = models.ImageField(upload_to='artisans/', blank=True, null=True)

    rating = models.FloatField(default=0)

    is_approved = models.BooleanField(default=False)
        

    def __str__(self):
        return self.name

# models.py
class Review(models.Model):
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)  # <--- جديد
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user_name} - {self.artisan.name}"

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



