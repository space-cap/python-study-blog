from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def sayHello(request, name):
    html = "<html><body>Hello, %s!</body></html>" % name
    return HttpResponse(html)


