from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User

from .models import Article

def index(request):
    post_list = Article.objects.filter(user=request.user) 
    #.order_by('-pub_date')[:5]
    context = {
        'post_list': post_list,
        'user': request.user,
    }
    return render(request, 'main/index.html', context)

def post(request, post_id):
    article = get_object_or_404(Article, pk=post_id)
    return render(request, 'main/post.html', {'article': article})

def users(request):
    user_list = User.objects.all()
    output = ', '.join([u.username + ': ' + str(u.pk) for u in user_list])
    return HttpResponse(output)