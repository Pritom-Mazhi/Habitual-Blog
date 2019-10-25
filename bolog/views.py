from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
    my_title = "Home Page"
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to Common Blog", 'blog_list': qs}
    return render(request, 'home.html', context)

def about_page(request):
    return render(request, 'about.html', {"title": "About Us"})

def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {"title": "Contact Us",
                'form': form
                }
    return render(request, 'form.html', context)

def example_page(request):
    context         = {"title": "Example Cxt"}
    template_name   = 'hello_world.html'
    template_object = get_template(template_name)
    rendered_object = template_object.render(context)
    return HttpResponse(rendered_object)
    #render(request, 'hello_world.html', {"title": "Contact Us"})
