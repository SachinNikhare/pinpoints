from venv import create
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from .models import pinpointsURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {"title":"Pinpoints.com","form":the_form}
        return render(request, 'shortener/home.html', context)
    
    def post(self, request, *args, **kwargs):
        # print(request.POST.get('url'))
        form = SubmitUrlForm(request.POST)
        context = {"title":"Pinpoints.com","form":form}
        template = "shortener/home.html"
        if form.is_valid():
            print(form.cleaned_data.get("url"))
            if 'http://' not in form.cleaned_data.get('url'):
                new_url = 'http://'+form.cleaned_data.get('url')
            else:
                new_url = form.cleaned_data.get('url')
            obj, created = pinpointsURL.objects.get_or_create(url=new_url)
            context = {"object":obj,"created":created}
            if created:
                template = 'shortener/success.html'
            else:
                template = 'shortener/already-exists.html'
        
        return render(request, template, context)

class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(pinpointsURL, shortcode=shortcode)
        qs = pinpointsURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count!=1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        # ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)