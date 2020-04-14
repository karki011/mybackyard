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
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})
    total_listing = len(post_listing)
    final_posting_result = []
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "N/A"

        if post.find('a').get('data-ids'):
            post_image_data_id = post.find('a').get('data-ids')
            image_id = str(post_image_data_id).split(',')
            single_image_id = image_id[0]
            final_image = BASE_IMAGE_URL.format(single_image_id[2:])
        else:
            final_image = 'https://craigslist.org/images/peace.jpg'
        final_posting_result.append(
            (post_title, post_url, post_price, final_image))

    frontend = {
        'search': search,
        'final_posting_result': final_posting_result,
        'total_listing': total_listing
    }
    return render(request, 'my_app/new_search.html', frontend)
