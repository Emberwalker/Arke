from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest

def index(req):
    return render(req, 'index.html')

def login(req):
    if req.method == 'POST':
        form = AuthenticationForm(req)
        print(form)
        if form.is_valid():
            return HttpResponseRedirect('/')

    elif req.method == 'GET':
        form = AuthenticationForm()
    else:
        return HttpResponseBadRequest()
    
    return render(req, 'login.html', {'form': form})
