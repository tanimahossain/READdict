from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book, Category, Profile, Read
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
def index(request):
    categories = Category.objects.all()[:15]
    return render(request, 'Reading/index.html', {'categories': categories})

def books(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'Reading/shop-grid.html', {'books': books, 'categories': categories})

def books_by_category(request, id):
    books = Book.objects.filter(category=id)
    categories = Category.objects.all()
    return render(request, 'Reading/shop-grid.html', {'books': books, 'categories': categories})

def single_book(request, id):
    found = Book.objects.filter(id=id).exists()
    if found is False:
        categories = Category.objects.all()
        return render(request, 'Reading/error404.html', {'categories': categories})
    book = Book.objects.get(id=id)
    categories = Category.objects.all()
    recents = Book.objects.order_by('-id')[:3]
    return render(request, 'Reading/single-product.html', {'book': book, 'categories': categories, 'recents': recents})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'Reading/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('pass')

        username = Profile.objects.get(email=email.lower()).user.username
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            msg = 'Success'
            data = {
                'msg': msg
            }
            return JsonResponse(data)

        else:
            msg = 'Incorrect Password'
            data = {
                'msg': msg
            }
            return JsonResponse(data)

def check_user(request):
    email = request.GET.get('email', None)
    found = Profile.objects.filter(email__exact=email.lower()).exists()
    if found:
        msg = 'found'
        data = {
            'msg': msg
        }
        return JsonResponse(data)
    else:
        msg = 'No such user!'
        data = {
            'msg': msg
        }
        return JsonResponse(data)

def check_email(request):
    email = request.GET.get('email', None)
    found = Profile.objects.filter(email__exact=email.lower()).exists()
    if found:
        msg = 'Email already exists!'
        data = {
            'msg': msg
        }
        return JsonResponse(data)
    else:
        msg = 'ok'
        data = {
            'msg': msg
        }
        return JsonResponse(data)

def check_username(request):
    username = request.GET.get('username', None)
    found = Profile.objects.filter(user__username=username).exists()
    if found:
        msg = 'Username already exists!'
        data = {
            'msg': msg
        }
        return JsonResponse(data)
    else:
        msg = 'ok'
        data = {
            'msg': msg
        }
        return JsonResponse(data)

def signup(request):
    name = request.POST.get('name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('pass')

    user = User.objects.create_user(username=username, password=password)
    Profile.objects.create(user=user, email=email, name=name)

    msg = 'User successfully created!'
    data = {
        'msg': msg
    }

    return JsonResponse(data)

@login_required
def start_reading(request):
    user = request.POST.get('user')
    book = request.POST.get('book')
    target = request.POST.get('target')
    print('{} {} {}'.format(user, book, target))
    read = Read.objects.create(user_id=user, book_id=book, target=target)
    data = {
        'progress': read.progress
    }
    return JsonResponse(data)

@login_required
def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        categories = Category.objects.all()
        return render(request, 'Reading/my-account.html', {'profile': profile, 'categories': categories})
    else:
        categories = Category.objects.all()
        return render(request, 'Reading/error404.html', {'categories': categories})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))