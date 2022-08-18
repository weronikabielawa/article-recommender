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
import plotly.express as ex


# Create your views here.
def recommender(request):
    context = {}
    if request.method == 'POST':

        # restarting heroku dynos, so the app doesn't crash
        heroku_conn = heroku3.from_key('ef02e4cf-7d5f-4590-aab6-7e9ca8ecb3b8')
        app = heroku_conn.apps()['boiling-lowlands-72442']
        app.restart()

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
                form = Results()
                #return HttpResponse('Należy ocenić wszystkie propozycje!')


            else:
                new_result = ResultsModel(propozycja_1=propozycja_1, propozycja_2=propozycja_2, propozycja_3=propozycja_3)
                new_result.save()
                #messages.success(request, 'Dziękuję za ocenę! :) ')
                return HttpResponseRedirect('/thank_you')

    else:
        form = Results()
        context['form'] = form

    return render(request, "results.html", context)


def thank_you(request):
    return render(request, "thank_you.html")


def charts(request):
    #ResultsModel.objects.all().delete()
    data_for_chart = ResultsModel.objects.all()

    results_1 = [i.propozycja_1 for i in data_for_chart]
    results_2 = [i.propozycja_2 for i in data_for_chart]
    results_3 = [i.propozycja_3 for i in data_for_chart]

    print(results_1)
    #print(type(data_for_chart[0]))
    x_1 = [i for i in set(results_1)]
    y_1 = [results_1.count(i) for i in set(results_1)]

    ex.bar(x=x_1, y=y_1).write_image("static/charts/results1.png")

    x_2 = [i for i in set(results_2)]
    y_2 = [results_2.count(i) for i in set(results_2)]

    ex.bar(x=x_2, y=y_2).write_image("static/charts/results2.png")

    x_3 = [i for i in set(results_3)]
    y_3 = [results_3.count(i) for i in set(results_3)]

    ex.bar(x=x_3, y=y_3).write_image("static/charts/results3.png")
    return render(request, "charts.html")