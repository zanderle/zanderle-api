import requests
import xmltodict

from django.http import JsonResponse
from django.conf import settings


def user_index(request):
    username = request.GET['username']

    data = {
        'username': username,
        'key': settings.GOODREADS_API_KEY
    }
    r = requests.get('https://www.goodreads.com/user/show/', data)

    gr_response = xmltodict.parse(r.text)

    user = gr_response['GoodreadsResponse']['user']

    fields = ['name', 'link', 'image_url', 'user_name', 'id']

    response = {}
    for field in fields:
        response[field] = user[field]

    return JsonResponse(response)


def books_read_shelf(request):
    user_id = request.GET['id']

    data = {
        'id': user_id,
        'shelf': 'read',
        'v': 2,
        'per_page': 200,
        'key': settings.GOODREADS_API_KEY
    }
    r = requests.get('https://www.goodreads.com/review/list/', data)

    gr_response = xmltodict.parse(r.text)

    books = gr_response['GoodreadsResponse']['reviews']['review']

    book_fields = ['title', 'link', 'image_url', 'num_pages', 'publication_year', 'authors']
    fields = ['started_at', 'read_at']

    response = []
    for book in books:
        book_response = {}
        for field in book_fields:
            book_response[field] = book['book'][field]
        for field in fields:
            book_response[field] = book[field]

        response.append(book_response)

    return JsonResponse(response, safe=False)
