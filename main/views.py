from django.shortcuts import render
from django.http import HttpResponse

from .models import Article

def index(request):
    latest_post_list = Article.objects.order_by('-pub_date')[:5]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'main/index.html', context)

def post(request, post_id):
    return HttpResponse("You're looking at post %s." % post_id)