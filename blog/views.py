from .models import Post
from .forms import PostForm

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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

def create_post(rqst):
    form = PostForm(rqst.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
        return HttpResponseRedirect(inst.get_absolute_url())
    return render(rqst, 'blog/postform.html', context)

def update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'blog/postform.html', context)