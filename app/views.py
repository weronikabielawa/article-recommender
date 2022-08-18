from django.shortcuts import render
from .forms import InputForm, Results
from django.http import HttpResponseRedirect, HttpResponse
from .models import ResultsModel
from django.contrib import messages

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

        # restarting heroku dynos, so the app doesn't crash
        #heroku_conn = heroku3.from_key('ef02e4cf-7d5f-4590-aab6-7e9ca8ecb3b8')
        #app = heroku_conn.apps()['boiling-lowlands-72442']
        #app.restart()

        form = InputForm(request.POST)
        if form.is_valid():

            context['form'] = form
            article_preprocessed = preprocess(pd.DataFrame({'page_content': [form.cleaned_data['treść_artykułu']]}))
            tfidf = train_and_recommend(article_preprocessed)
            request.session['result_1'] = tfidf

            tok2vec_pre = recommend(article_preprocessed)
            request.session['result_2'] = tok2vec_pre

            doc2vec = recommend_doc2vec(article_preprocessed)
            request.session['result_3'] = doc2vec

            #return results(request, context=context)
            return HttpResponseRedirect('/results/')
            #return render(request, "results.html", context)

    else:
        form = InputForm()

    context['form'] = form
    return render(request, "recommender.html", context)



# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def results(request, context={}):
    context['result_1'] = request.session.get('result_1')
    context['result_2'] = request.session.get('result_2')
    context['result_3'] = request.session.get('result_3')
    #del request.session['result_1']
    #del request.session['result_2']
    #del request.session['result_3']

    if request.method == 'POST':
        form = Results(request.POST)
        if form.is_valid():

            propozycja_1 = int(form['propozycja_1'].data)
            propozycja_2 = int(form['propozycja_2'].data)
            propozycja_3 = int(form['propozycja_3'].data)
            print((propozycja_1, propozycja_2, propozycja_3))

            if 0 in [propozycja_2, propozycja_3, propozycja_1]:
                print('wrong input ')
                messages.error(request, 'Należy ocenić wszystkie propozycje!')
                #return HttpResponse('Należy ocenić wszystkie propozycje!')


            else:
                new_result = ResultsModel(propozycja_1=propozycja_1, propozycja_2=propozycja_2, propozycja_3=propozycja_3)
                new_result.save()
                #messages.success(request, 'Dziękuję za ocenę! :) ')
                return HttpResponseRedirect('/thank_you')

                del form

    else:
        form = Results()
        context['form'] = form

    return render(request, "results.html", context)


def thank_you(request):
    return render(request, "thank_you.html")