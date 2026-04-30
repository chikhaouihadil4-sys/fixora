from django.db import models
from django.contrib.auth.models import User


class Artisan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    experience = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='artisans/', blank=True, null=True)

    rating = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Service(models.Model):
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name="services")

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Review(models.Model):
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user_name} - {self.artisan.name}"




class Complaint(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    service = models.CharField(max_length=100)
    reason = models.CharField(max_length=200)
    description = models.TextField()

    attachment = models.FileField(upload_to='complaints/', null=True, blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sent_complaints"
    )

    artisan = models.ForeignKey(
        'Artisan',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="complaints"
    )

    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_complaints"
    )

    sender_type = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('artisan', 'Artisan')],
        default='user'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
    
    
class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)

class BlackList(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    artisan = models.ForeignKey(Artisan, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    
    