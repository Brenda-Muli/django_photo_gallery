from django.shortcuts import render, redirect, get_object_or_404
from .forms import PictureForm, DisplayForm
from .models import Gallery
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout


# Create your views here.

# User Registration view
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
       form = RegisterForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('login')
    context = {'registerform': form}
    return render(request, 'register.html', context=context)
    

#User Login view
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    context = {'loginform':form}
    return render(request, 'login.html', context=context)

#Home view
@login_required(login_url = 'login')
def home (request):
    category = request.GET.get('category', None)
    if category:
        pictures = Gallery.objects.filter(tag_category=category)
    else:
        pictures = Gallery.objects.all()
    return render(request, 'home.html', {'pictures': pictures})

#Add picture view
@login_required(login_url = 'login')
def add_pic(request):
  if request.method == 'POST':
    add_picture = PictureForm(request.POST, request.FILES)
    if add_picture.is_valid():
        picture = add_picture.save(commit = False) #saving picture, but not to database
        picture.user = request.user #associating picture with the user
        picture.save() #saving to the user-database
        add_picture.save_m2m() #saves form using many to many relations
        messages.success(request, 'Image uploaded successfully!')
        return redirect('home') #redirect home page
    else:
      messages.error(request, 'Error occured during uplaod')
  else:
    add_picture = PictureForm()
  return render(request, 'add_pic.html',{'add_picture': add_picture})

#Picture detail view
@login_required(login_url = 'login')
def picture_detail(request, pic_id):
    pic = get_object_or_404(Gallery, id = pic_id)
    form = DisplayForm(instance=pic)
    if request.method == 'POST':
      if request.user in pic.likes.all():
            pic.likes.remove(request.user)  # Remove like
            messages.success(request, 'You unliked this picture.')
      else:
            pic.likes.add(request.user)  # Add like
            messages.success(request, 'You liked this picture.')

    return render(request, 'pic_detail.html', {'form': form, 'pic': pic})

#Logout
def logout(request):
    auth_logout(request)
    return redirect('login')

    