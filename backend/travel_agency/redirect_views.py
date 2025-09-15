# Simple redirect view
from django.http import HttpResponseRedirect

def home_redirect(request):
    return HttpResponseRedirect('/login/')