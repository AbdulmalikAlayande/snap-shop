from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def say_hello(request):
    my_names = ['Abdulmalik', 'Ayanniyi', 'Abolade', 'Alabi']
    return render(request, "hello.html", {'name':my_names})
