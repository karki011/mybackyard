import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
# Create your views here.

BASE_URL = 'https://bham.craigslist.org/search/sss?query={}'


def home(request):
    print('view.home')
    return render(request, "base.html")


def new_search(request):
    print('view.search')
    search = request.POST.get('search')
    response = requests.get(
        'https://bham.craigslist.org/search/sss?query=python')
    data = response.text
    print(data)
    frontend = {
        'search': search
    }
    return render(request, 'my_app/new_search.html', frontend)
