from django.shortcuts import render, HttpResponseRedirect
from blog.forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import Group

# Home views function here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

#About
def about(request):
    return render(request, 'blog/about.html')

#About
def contact(request):
    return render(request, 'blog/contact.html')

#Dashbord
def user_dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        # view profile 
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts, 'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            messages.success(request, 'Congratulations! Your account has been created successfully. ')
            user = form.save()
            group = Group.objects.get(name='Author')   #Create account set group member
            user.groups.add(group)
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form':form})

#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)

            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']

                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successfully !')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


#Add Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)

            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#Edit/Updat Post
def updat_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)

            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
#Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
