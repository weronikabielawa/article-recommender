from django.shortcuts import render
from .forms import InputForm
from django.http import HttpResponseRedirect, HttpResponse
from src.models.tfidf import *


# Create your views here.
def home_view(request):
    context = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InputForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            x = train_and_recommend(form.cleaned_data['article_content'])
            print(x)
            print(type(form.cleaned_data))
            #return HttpResponseRedirect('/')
            context['form'] = form
            context['result'] = x.tolist()[0]
            return render(request, "home.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InputForm()

    context['form'] = form
    return render(request, "home.html", context)


def results(request, recom):
    print("im here")
    #render(request, "recom")
    #pass
#from .models import Greeting

# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def recommender(request):
    return render(request, "recommender.html")


