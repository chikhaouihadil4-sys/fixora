from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth import login, authenticate, logout
from .models import Artisan, Review
from .forms import ReviewForm, ArtisanRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# الصفحة الرئيسية
def home(request):
    
    services = Artisan.objects.values_list('service', flat=True).distinct()
    cities = Artisan.objects.values_list('city', flat=True).distinct()
    top_artisans = Artisan.objects.filter(is_approved=True).order_by('-rating')[:4]

    return render(request, 'main/index.html', {
        'services': services,
        'cities': cities,
        'top_artisans': top_artisans
       
    })


# تسجيل المستخدم
def register_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # التحقق من تطابق الباسوورد
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'main/register_user.html')

        # التحقق من وجود الاسم مسبقاً
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'main/register_user.html')

        # التحقق من وجود الإيميل مسبقاً
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'main/register_user.html')

        # إنشاء اليوزر
        User.objects.create_user(username=name, email=email, password=password)

        # رسالة نجاح
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')  # تحويل المستخدم لصفحة تسجيل الدخول

    # إذا كان request GET
    return render(request, 'main/register_user.html')
def register_artisan(request):
    if request.method == 'POST':
        form = ArtisanRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            artisan = form.save(commit=False)
            artisan.is_approved = False  # لازم الادمين يقبل التسجيل
            artisan.save()
            return redirect('home')  # ولا صفحة شكراً لك
    else:
        form = ArtisanRegisterForm()
    return render(request, 'main/register_artisan.html', {'form': form})

# تسجيل الدخول


def login_user(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Email or password is incorrect!")
            return render(request, "main/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email or password is incorrect!")
            return render(request, "main/login.html")

    return render(request, "main/login.html")
# نتائج البحث
def results(request):

    service = request.GET.get('service')
    city = request.GET.get('city')

    artisans = Artisan.objects.filter(is_approved=True)

    if service:
        artisans = artisans.filter(service__icontains=service)

    if city:
        artisans = artisans.filter(city__icontains=city)

    for artisan in artisans:

        avg = Review.objects.filter(artisan=artisan).aggregate(Avg('rating'))['rating__avg']

        artisan.average_rating = round(avg, 1) if avg else 0

    return render(request, 'main/results.html', {'artisans': artisans})


# صفحة البروفايل
@login_required
def profile(request, id):
    artisan = get_object_or_404(Artisan, id=id)

    reviews = Review.objects.filter(artisan=artisan)

    avg = reviews.aggregate(Avg('rating'))['rating__avg']

    average_rating = round(avg, 1) if avg else 0

    return render(request, 'main/profile.html', {
        'artisan': artisan,
        'reviews': reviews,
        'average_rating': average_rating
    })


# إضافة review
def add_review(request, id):

    artisan = get_object_or_404(Artisan, id=id)

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.artisan = artisan

            review.save()

            avg = Review.objects.filter(artisan=artisan).aggregate(Avg('rating'))['rating__avg']

            artisan.rating = round(avg, 1) if avg else 0

            artisan.save()

            return redirect('profile', id=artisan.id)

    else:

        form = ReviewForm()

    return render(request, 'main/add_review.html', {
        'form': form,
        'artisan': artisan
    })


# صفحة البحث
def search_results(request):

    service = request.GET.get('service')
    city = request.GET.get('city')

    artisans = Artisan.objects.filter(is_approved=True)

    if service:
        artisans = artisans.filter(service__icontains=service)

    if city:
        artisans = artisans.filter(city__icontains=city)

    return render(request, 'main/search_results.html', {'artisans': artisans})


def logout_user(request):
    logout(request)
    return redirect('home')




