from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from posts.models import Post, Category
from posts.forms import PostForm, LoginForm


def index(request):
    category_data = request.GET.get("category_form")
    # print(category_data)
    if category_data == None or category_data == "0":
        values = Post.objects.all()
    else:
        values = Post.objects.filter(category=category_data)
    date_sort_date = request.GET.get("date_sort_form")
    if date_sort_date == "new":
        values = values.order_by("-datetime_created")
    else:
        values = values.order_by("datetime_created")
    categories = Category.objects.all()
    if category_data:
        category_data =  int(category_data)
    return render(request, 'index.html', {'posts':values, "categories":categories, "selected_category":category_data, "selected_data_sort":date_sort_date})


def post(request):
    if request.method == "POST" and request.user.is_authenticated:
        print(request.POST)
        header_data = request.POST.get("header_form")
        text_data = request.POST.get("text_form")
        category_data = request.POST.get("category_form")
        category = Category.objects.get(id=category_data)
        file_data = request.FILES.get("file_form")
        user = request.user
        if header_data and text_data:
            Post.objects.create(header=header_data, text=text_data, category=category, image=file_data, author=user)
            return redirect("index")
    categories = Category.objects.all()
    return render(request, 'post.html', {"categories":categories})


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST" and request.user == post.author:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            post.header = data.get('header') 
            post.text = data.get('text')
            post.category = data.get('category')
            if data.get('image'):
                post.image.delete()
                post.image = data.get('image')
            post.save()
            return redirect("index")
    form = PostForm({'header': post.header, 
                     'category': post.category, 
                     'text': post.text, 
                     'image': post.image,
                     'uploaded_image': post.image.url})
    return render(request, 'edit_post.html', {"form": form})


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST" and request.user == post.author:
        post.delete()
        return redirect("index")
    return render(request, 'delete_post.html', {"post": post})


def user_login(request):
    error = ""
    if request.method == 'POST':
        username_data = request.POST['username']
        password_data = request.POST['password']
        user = authenticate(username=username_data, password=password_data)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error = 'Неверное имя пользователя или пароль.'
    form = LoginForm()
    return render(request, 'login.html', {"form": form, "error":error})


def user_logout(request):
    logout(request)
    return redirect('index')