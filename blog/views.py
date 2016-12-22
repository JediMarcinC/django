from .models import Post
from .forms import PostForm

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def s(request):
    return HttpResponse("<h1>Hello</h1>")

def demo(request):
    return render(request, 'demo_static.html')

def some(rq):
    return HttpResponse("<h2>Some text here</h2>")

def index(rqst):
    post_list = Post.objects.all().order_by('-created_date')
    paginator = Paginator(post_list, 6) # Show 8 contacts per page
    page = rqst.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(rqst, 'blog/index.html', {'objects': posts})


def detail(rq, id):
    # object = Post.objects.get(id=id)
    object = get_object_or_404(Post, id=id)
    return render(rq, 'blog/detail.html', {'obj': object})

def create_post(rqst):
    form = PostForm(rqst.POST or None, rqst.FILES or None)
    context = {
        'form': form
    }
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
        messages.success(rqst, 'Succesfully created! Congratulations!')
        return HttpResponseRedirect(inst.get_absolute_url())
    else:
        messages.error(rqst, "Unfortunately entry couldn't be created")
    return render(rqst, 'blog/postform.html', context)

def update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
        messages.success(request, 'Succesfully changed! Congratulations!')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request, "Unfortunately entry couldn't be changed")
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'blog/postform.html', context)

def delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Succesfully deleted')
    return redirect("posts:index")

