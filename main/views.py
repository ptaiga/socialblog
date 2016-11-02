from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Article

def index(request):
    latest_post_list = Article.objects.order_by('-pub_date')[:5]
    context = {
        'latest_post_list': latest_post_list,
        'user': request.user,
    }
    return render(request, 'main/index.html', context)

def post(request, post_id):
    article = get_object_or_404(Article, pk=post_id)
    return render(request, 'main/post.html', {'article': article})