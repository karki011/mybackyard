from django.shortcuts import render
# Create your views here.


def home(request):
    print('this is home')
    return render(request, "base.html")


def new_search(request):
    print('this is new search')

    return render(request, 'my_app/new_search.html', )
