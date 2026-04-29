from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_protect
from .models import Artisan, Review, Service, ServiceRequest, Complaint, BlackList 
from .forms import ReviewForm, ServiceRequestForm, ComplaintForm
from django.http import HttpResponse



# ---------------- HOME ----------------
def home(request):
    services = Service.objects.values_list('name', flat=True).distinct()
    cities = Artisan.objects.values_list('city', flat=True).distinct()

    top_artisans = Artisan.objects.filter(
        status='accepted',
        is_blocked=False
    ).order_by('-rating')[:4]

    return render(request, 'main/index.html', {
        'services': services,
        'cities': cities,
        'top_artisans': top_artisans
    })


# ---------------- REGISTER USER ----------------
def register_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register_user")

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken!")
            return redirect("register_user")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register_user")

        User.objects.create_user(username=name, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'main/register_user.html')


# ---------------- REGISTER ARTISAN ----------------
def register_artisan(request):
    if request.method == "POST":

        username = request.POST.get("username")
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        city = request.POST.get("city")
        phone = request.POST.get("phone")
        experience = request.POST.get("experience")
        description = request.POST.get("description")

        image = request.FILES.get("image")  # ← مهم جدًا

        count = int(request.POST.get("services_count", 0))

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_artisan")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register_artisan")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        artisan = Artisan.objects.create(
            user=user,
            name=full_name,
            email=email,
            city=city,
            phone=phone,
            experience=experience or 0,
            description=description,
            image=image,  # ← مهم جدًا
            status="pending",
            is_blocked=False
        )

        for i in range(count):
            name = request.POST.get(f"service_{i}")
            price = request.POST.get(f"price_{i}")

            if name:
                Service.objects.create(
                    artisan=artisan,
                    name=name,
                    price=price or 0
                )

        return redirect("home")

    return render(request, "main/register_artisan.html")
# ---------------- LOGIN ----------------



@csrf_protect
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            artisan = Artisan.objects.filter(user=user).first()

            if artisan:
                if artisan.is_blocked:
                    messages.error(request, "Account blocked")
                    logout(request)
                    return redirect("login")

                if artisan.status != "accepted":
                    messages.error(request, "Account not approved yet")
                    logout(request)
                    return redirect("login")

                return redirect("profile", id=artisan.id)

            return redirect("home")

        messages.error(request, "Invalid credentials")
        return redirect("login")

    return render(request, "main/login.html")
# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('home')




# ---------------- PROFILE ----------------
@login_required
def profile(request, id):
    artisan = get_object_or_404(Artisan, id=id)

    reviews = Review.objects.filter(artisan=artisan)
    avg = reviews.aggregate(Avg('rating'))['rating__avg']
    average_rating = round(avg, 1) if avg else 0

    services = Service.objects.filter(artisan=artisan)

    is_owner = request.user == artisan.user

    return render(request, 'main/profile.html', {
        'artisan': artisan,
        'reviews': reviews,
        'average_rating': average_rating,
        'services': services,
        'is_owner': is_owner
    })


# ---------------- ADD REVIEW ----------------
@login_required
def add_review(request, id):
    artisan = get_object_or_404(Artisan, id=id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.artisan = artisan
            review.user = request.user
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

# ---------------- SEARCH ----------------
def search_results(request):
    
    service = request.GET.get('service', '').strip()
    city = request.GET.get('city', '').strip()

    artisans = Artisan.objects.filter(
        status='accepted',
        is_blocked=False
    )

    if service:
        artisans = artisans.filter(
            services__name__icontains=service
        )

    if city:
        artisans = artisans.filter(
            city__icontains=city
        )

    for artisan in artisans:
        try:
            avg = Review.objects.filter(
                artisan=artisan
            ).aggregate(Avg('rating'))['rating__avg']

            artisan.average_rating = round(avg, 1) if avg else 0

        except Exception as e:
            print("ERROR IN RATING:", e)
            artisan.average_rating = 0

    return render(request, 'main/search_results.html', {
        'artisans': artisans.distinct(),
        'service': service,
        'city': city
    })



# ---------------- REQUEST SERVICE ----------------
@login_required
def request_service(request, id):
    artisan = get_object_or_404(Artisan, id=id)

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, artisan=artisan)

        if form.is_valid():
            req = form.save(commit=False)
            req.artisan = artisan
            req.user = request.user
            req.save()
            print("SAVED ✅")

            return redirect('profile', id=artisan.id)

        else:
            print("FORM ERRORS ❌", form.errors)

    else:
        form = ServiceRequestForm(artisan=artisan)

    return render(request, 'main/request_service.html', {
        'artisan': artisan,
        'form': form
    })
# ---------------- ARTISAN REQUESTS ----------------
@login_required
def artisan_requests(request):
    artisan = Artisan.objects.filter(user=request.user).first()

    if not artisan:
        return render(request, "main/artisan_requests.html", {
            "requests": []
        })

    requests = ServiceRequest.objects.filter(
        artisan=artisan
    ).order_by('-created_at')

    return render(request, "main/artisan_requests.html", {
        "requests": requests
    })
    
# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    artisan = get_object_or_404(Artisan, user=request.user)

    if request.method == "POST":
        artisan.name = request.POST.get("name")
        artisan.phone = request.POST.get("phone")
        artisan.city = request.POST.get("city")
        artisan.email = request.POST.get("email")
        artisan.experience = request.POST.get("experience")
        artisan.description = request.POST.get("description")

        if "image" in request.FILES:
            artisan.image = request.FILES["image"]

        artisan.save()

        return redirect("profile", id=artisan.id)

    return render(request, "main/edit_profile.html", {"artisan": artisan})

# ---------------- HISTORY ----------------
@login_required
def user_history(request):
    requests = ServiceRequest.objects.filter(
    user=request.user
    ).order_by('-created_at')
    return render(request, 'main/user_history.html', {'requests': requests})


@login_required
def artisan_history(request):
    artisan = Artisan.objects.filter(user=request.user).first()

    if not artisan:
        return render(request, 'main/artisan_history.html', {'requests': []})

    requests = ServiceRequest.objects.filter(artisan=artisan).order_by('-created_at')
    return render(request, 'main/artisan_history.html', {'requests': requests})

# ---------------- COMPLAINTS ----------------

@login_required
def send_complaint(request, target_type, id):
    target_artisan = None
    target_user = None

    if target_type == "artisan":
        target_artisan = get_object_or_404(Artisan, id=id)

    elif target_type == "user":
        target_user = get_object_or_404(User, id=id)

    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():
            complaint = form.save(commit=False)

            complaint.user = request.user
            complaint.artisan = target_artisan
            complaint.target_user = target_user
            complaint.sender_type = "user"
            complaint.status = "pending"

            complaint.save()

            return redirect("complaints_history")

        else:
            return HttpResponse(form.errors)

    else:
        form = ComplaintForm()

    return render(request, "main/send_complaint.html", {
        "form": form,
        "artisan": target_artisan,
        "target_user": target_user,
        "target_type": target_type
    })
@login_required
def complaints_history(request):
    complaints = Complaint.objects.filter(
        Q(user=request.user) |
        Q(artisan__user=request.user) |
        Q(target_user=request.user)
    ).distinct().order_by('-created_at')

    return render(request, "main/complaints_history.html", {
        "complaints": complaints
    })
# ---------------- ADMIN DASHBOARD ----------------
@staff_member_required
def admin_dashboard(request):
    return render(request, 'main/admin/dashboard.html', {
        'users': User.objects.all(),
        'artisans': Artisan.objects.all(),
        'reviews': Review.objects.all(),
        'complaints': Complaint.objects.all(),
        'request_service': ServiceRequest.objects.all(),

        'users_count': User.objects.count(),
        'artisans_count': Artisan.objects.count(),
        'reviews_count': Review.objects.count(),
        'complaints_count': Complaint.objects.count(),
        'service_requests_count': ServiceRequest.objects.count(),
    })


# ---------------- ADMIN ARTISANS APPROVAL ----------------
@staff_member_required
def accept_artisan(request, id):
    artisan = get_object_or_404(Artisan, id=id)
    artisan.status = 'accepted'
    artisan.save()
    return redirect('admin_dashboard')


@staff_member_required
def reject_artisan(request, id):
    artisan = get_object_or_404(Artisan, id=id)
    artisan.status = 'rejected'
    artisan.is_blocked = True
    artisan.save()

    BlackList.objects.create(
        artisan=artisan,
        reason="Rejected by admin"
    )

    return redirect('admin_dashboard')

# ---------------- SERVICE REQUEST ACTIONS ----------------
@login_required
def accept_request(request, id):
    req = get_object_or_404(ServiceRequest, id=id)

    # لازم يكون الطلب مربوط بالـ artisan
    if req.artisan.user != request.user:
        return redirect('home')

    req.status = "accepted"
    req.save()
    return redirect('artisan_requests')

@login_required
def reject_request(request, id):
    req = get_object_or_404(ServiceRequest, id=id)

    if req.artisan.user != request.user:
        return redirect('home')

    req.status = "rejected"
    req.save()
    return redirect('artisan_requests')


# ---------------- COMPLAINTS ACTIONS ----------------
@staff_member_required
def accept_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = "accepted"
    complaint.save()

    if complaint.artisan:
        complaint.artisan.is_blocked = True
        complaint.artisan.save()

        BlackList.objects.get_or_create(
            artisan=complaint.artisan,
            defaults={"reason": "Blocked via complaint"}
        )

    if complaint.user:
        complaint.user.is_active = False
        complaint.user.save()

        BlackList.objects.get_or_create(
            user=complaint.user,
            defaults={"reason": "Blocked via complaint"}
        )

    return redirect("admin_dashboard")


@staff_member_required
def reject_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = "rejected"
    complaint.save()
    return redirect("admin_dashboard")


# ---------------- BLOCK SYSTEM ----------------
@staff_member_required
def block_artisan(request, id):
    artisan = get_object_or_404(Artisan, id=id)
    artisan.is_blocked = True
    artisan.save()

    BlackList.objects.create(artisan=artisan, reason="Blocked by admin")
    return redirect('admin_dashboard')


@staff_member_required
def unblock_artisan(request, id):
    artisan = get_object_or_404(Artisan, id=id)
    artisan.is_blocked = False
    artisan.save()
    return redirect('admin_dashboard')


@staff_member_required
def block_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()

    BlackList.objects.create(user=user, reason="Blocked by admin")
    return redirect('admin_dashboard')
@staff_member_required
def unblock_user(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    return redirect('admin_dashboard')

