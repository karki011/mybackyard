import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.

BASE_URL = 'https://bham.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    print('view.home')
    return render(request, "base.html")


def new_search(request):
    print('view.search')
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_posting_result = []
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "N/A"

        post_image_data_id = post.find('a').get('data-ids')
        image_id = str(post_image_data_id).split(',')
        single_image_id = image_id[0]
        # print('s1', single_image_id)
        final_image = single_image_id[2:]

        final_posting_result.append(
            (post_title, post_url, post_price, final_image))

    frontend = {
        'search': search,
        'final_posting_result': final_posting_result,
    }
    return render(request, 'my_app/new_search.html', frontend)
