from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
# Create your views here
from .forms import BlogPostModelForm
from .models import BlogPost

# get -> 1 object
#filter -> [] objects

def blog_post_detail_page(request, slug):
    # queryset = BlogPost.objects.filter(slug=slug)
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog_post_detail.html'
    context = {"object": obj} #{"title": obj.title}
    return render(request, template_name, context)

#CRUD
def blog_post_list_view(request):
    #list out objects -> retrieve - several objects
    #could be search view
    qs = BlogPost.objects.all().published() #python list
    template_name = 'blog/list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

# @login_required
@staff_member_required
def blog_post_create_view(request):
    #create objects
    #how? use a form
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        #print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
        # obj = BlogPost.objects.create(**form.cleaned_data)
        # #for each key:value pairs to argument
        # # obj2 = OtherModel.objects.create(matha="title") #for 1 value
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

def blog_post_detail_view(request, slug):
    # 1 object -> retrieve - 1 object
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj} #{"title": obj.title}
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
    #based on original object
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    #based on the object, we pass our form an instance of the object
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj, 'form': None} #{"title": obj.title}
    return render(request, template_name, context)
