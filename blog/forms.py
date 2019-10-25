from django import forms

from .models import BlogPost

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
    class Meta:
        #if change the form but not the model, then write the override code line here
        #ie:title = forms.CharField() while 'BlogPost'model' title has 'models.TextField()'
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date'] #fields for models.py BlogPost model
        #based on a model itself and you just specify which fields from that model you
        ##want to include

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title') # 'title' in fields[] above
        qs = BlogPost.objects.filter(title__iexact=title) #__iexact or __icontains
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) #id=instance.id
        if qs.exists():
            raise forms.ValidationError("This title already used, please try another one")
        return title
