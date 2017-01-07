from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote_plus
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .models import Post
from .forms import PostForm

def s(request):
    return HttpResponse("<h1>Hello</h1>")

def demo(request):
    return render(request, 'demo_static.html')

def some(rq):
    return HttpResponse("<h2>Some text here</h2>")

def index(rqst):
    post_list = Post.objects.all().order_by('-created_date')
    page = rqst.GET.get('page')
    query = rqst.GET.get('qry')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
    paginator = Paginator(post_list, 6) # Show 8 contacts per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(rqst, 'blog/index.html', {'objects': posts, 'user':rqst.user})


def detail(rq, slug=None):
    # object = Post.objects.get(id=id)
    object = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(object.text)
    comments = Comment.objects. filter_by_instance(object)
    return render(rq, 'blog/detail.html', {'obj': object, 'share_string': share_string, 'comments': comments})

def create_post(rqst):
    if not rqst.user.is_staff and not rqst.user.is_superuser:
        raise Http404
    form = PostForm(rqst.POST or None, rqst.FILES or None)
    context = {
        'form': form
    }
    if form.is_valid():
        inst = form.save(commit=False)
        inst.user = rqst.user
        inst.save()
        messages.success(rqst, 'Succesfully created! Congratulations!')
        return HttpResponseRedirect(inst.get_absolute_url())
    return render(rqst, 'blog/postform.html', context)

def update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
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

def delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Succesfully deleted')
    return redirect("posts:index")

