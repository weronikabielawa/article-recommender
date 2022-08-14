from django.shortcuts import render
from .forms import InputForm
from django.http import HttpResponseRedirect, HttpResponse

import pandas as pd

from src.models.tfidf import train_and_recommend
from src.models.tok2vec_pretrained import recommend
from src.models.trained_word2vec import recommend_doc2vec
from src.preprocessing.preprocessing import preprocess
import heroku3


# Create your views here.
def recommender(request):
    context = {}
    if request.method == 'POST':
        heroku_conn = heroku3.from_key('ef02e4cf-7d5f-4590-aab6-7e9ca8ecb3b8')
        app = heroku_conn.apps()['boiling-lowlands-72442']
        app.restart()
        form = InputForm(request.POST)
        if form.is_valid():

            context['form'] = form
            article_preprocessed = preprocess(pd.DataFrame({'page_content': [form.cleaned_data['treść_artykułu']]}))
            tfidf = train_and_recommend(article_preprocessed)
            context['result_1'] = tfidf

            tok2vec_pre = recommend(article_preprocessed)
            context['result_2'] = tok2vec_pre

            doc2vec = recommend_doc2vec(article_preprocessed)
            context['result_3'] = doc2vec


            return render(request, "recommender.html", context)

    else:
        form = InputForm()

    context['form'] = form
    return render(request, "recommender.html", context)



# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    return render(request, "index.html")



