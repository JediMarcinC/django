from .models import Post

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def s(request):
    return HttpResponse("<h1>Hello</h1>")

def demo(request):
    return render(request, 'demo_static.html')

def some(rq):
    return HttpResponse("<h2>Some text here</h2>")

def index(rq):
    posts = Post.objects.all()
    return render(rq, 'blog/index.html', {'objects': posts})

def detail(rq, id):
    # object = Post.objects.get(id=id)
    object = get_object_or_404(Post, id=id)
    return render(rq, 'blog/detail.html', {'obj': object})