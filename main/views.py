from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Article

def index(request):
    subscribe_list = request.user.subscriber.subscribe_list.split(',')
    users = User.objects.filter(id__in = subscribe_list)
    post_list = Article.objects.filter(user__in=users).order_by('-pub_date')
    context = {
        'post_list': post_list,
        'user': request.user,
        'subscribe_list': subscribe_list,
        'users': users
    }
    return render(request, 'main/index.html', context)

def post(request, post_id):
    article = get_object_or_404(Article, pk=post_id)
    return render(request, 'main/post.html', {'article': article})

def new_post(request):
    return render(request, 'main/new_post.html', {})

def add_post(request):
    if (request.method == 'POST'):
        a = Article(\
            user=request.user,\
            header=request.POST['header'],\
            content=request.POST['content'],\
            pub_date=timezone.now())
        a.save()
        return HttpResponseRedirect(reverse('main:index', args=()))
    else:
        return HttpResponse('Something went wrong')

def users(request):
    user_list = User.objects.all()
    return render(request, 'main/users.html', {'user_list': user_list})
    #output = ', '.join([u.username + ': ' + str(u.pk) for u in user_list])
    #return HttpResponse(output)