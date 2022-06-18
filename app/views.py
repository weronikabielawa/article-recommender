from django.shortcuts import render
from .forms import InputForm
from django.http import HttpResponseRedirect, HttpResponse

import pandas as pd

from src.models.tfidf import train_and_recommend
from src.models.tok2vec_pretrained import recommend
from src.models.trained_word2vec import recommend_doc2vec
from src.preprocessing.preprocessing import preprocess


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
            article_preprocessed = preprocess(pd.DataFrame({'page_content': [form.cleaned_data['article_content']]}))
            #tfidf = train_and_recommend(article_preprocessed)
            context['form'] = form
            #context['result_1'] = tfidf.tolist()[0]

            tok2vec_pre = recommend(article_preprocessed)
            context['result_2'] = tok2vec_pre

            #doc2vec = recommend_doc2vec(article_preprocessed)
            #context['result_3'] = doc2vec


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


