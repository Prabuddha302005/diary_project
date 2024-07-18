from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from diaryapp.models import DairyEntry
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def homepage(request):
    return render(request, "home.html")


def user_register(request):
    data={}
    if(request.method=="POST"):
        uname = request.POST['username']
        upass = request.POST['password']
        cpass = request.POST['cpassword']
        print(uname, upass)
        
        if(uname=="" or upass=="" or cpass==""):
         data['error_msg'] = "fields cannot be empty"
         return render(request, 'register.html', context=data)
        elif(upass != cpass):
         data['error_msg'] = "Password did not match"
         return render(request, 'register.html', context=data)
        elif(User.objects.filter(username=uname).exists()):
         data['error_msg'] = uname+" username already exists"
         return render(request, 'register.html', context=data)
        else:
         user = User.objects.create(username=uname)
         user.set_password(upass)
         user.save()
         return redirect("/login")

    return render(request, "register.html")


def user_login(request):
   data={}
   if(request.method=="POST"):
      uname=request.POST['username']
      upass=request.POST['password']
      if(uname=="" or upass==""):
         # print("fields cant be empty")
         data['error_msg']="fields cant be empty"
         return render(request,'login.html',context=data)
      elif(not User.objects.filter(username=uname).exists()):
         # print(uname + " is already exist")
         data['error_msg']=uname + " is does not exist"
         return render(request,'login.html',context=data)
      else:
         user=authenticate(username=uname, password=upass)
         if user is None:
            data['error_msg']="Wrong password"
            return render(request, "login.html", context=data)
         else:
            login(request, user)
            messages.success(request, "Logged in ")
            return redirect('/show-entry')
   return render(request, "login.html")

def user_logout(request):
   logout(request)
   messages.error(request, "Logged out ")
   return redirect("/")


def add_entry(request):
   data={}
   if(request.user.is_authenticated):
    if(request.method=="POST"):
      title=request.POST['title']
      content=request.POST['content']
      print(title, content)

      if(title=="" or content==""):
         data['error_msg'] = "Please enter title and content"
         return render(request, "add_entry.html", context=data)
      else:
         user_id = request.user.id;
         user = User.objects.get(id=user_id)
         save_entry = DairyEntry.objects.create(title=title, content=content, uid=user)
         save_entry.save()
         
         messages.success(request, "Entry added successfully")
         return redirect("/show-entry")
   else:
      return redirect("/login")
   return render(request, "add_entry.html")


entries = DairyEntry.objects.none()
def show_entry(request):
   data={}
   global entries
   global filtered_date
   
   if(request.user.is_authenticated):
    show_entries = DairyEntry.objects.filter(uid=request.user.id)
    filtered_date = show_entries.order_by("-time")
   if(not filtered_date):
      data['error_msg'] = "No entries found"
      return render(request, 'show_entry.html', context=data)
   data['entry'] = filtered_date
    
   return render(request, "show_entry.html", context=data)
   
   
def delete_entry(request, entry_id):
   delete_entry = DairyEntry.objects.get(id=entry_id)
   delete_entry.delete()
   messages.error(request, "Entry deleted")
   return redirect("/show-entry")
   
def update_entry(request, entry_id):
   data={}
   entry = DairyEntry.objects.filter(id=entry_id)
   data['entry'] = entry[0]
   if(request.method=="POST"):
      title=request.POST['title']
      content=request.POST['content']
      print(title, content)

      if(title=="" or content==""):
         data['error_msg'] = "Please enter title and content"
         return render(request, "add_entry.html", context=data)
      else:
         entry = DairyEntry.objects.filter(id=entry_id)
         entry.update(title=title, content=content)
         messages.success(request, "Entry updated")
         return redirect("/show-entry")
   return render(request, "update_entry.html", context=data)
   
def filter_by_date(request, flag):
   global filtered_date
   data={}
   if(flag=='asc'):
      sorted_date = filtered_date.order_by("-time")
      
   else:
      sorted_date = filtered_date.order_by("time")
      
   data['entry'] = sorted_date
   return render(request, 'show_entry.html', context=data)


def search(request):
   data={}
   if(request.method=="POST"):
      entry_name = request.POST['entry_name']
      print(entry_name)
      filtered_date = DairyEntry.objects.filter(uid=request.user.id)
      searched_products = filtered_date.filter(Q(title__icontains=entry_name))
      if(not searched_products):
         data['error_msg'] = "No entries found"
         return render(request, 'show_entry.html', context=data)
      data['entry']=searched_products
      return render(request, 'show_entry.html', context=data)
   return render(request, 'show_entry.html')
