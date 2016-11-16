from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core import mail

from django.contrib.auth.models import User

from .models import Article

def index(request):
    subscribe_list = request.user.subscriber.subscribe_list.split(',')
    if (subscribe_list == ['']): subscribe_list = []
    subscriptions = User.objects.filter(id__in = subscribe_list)
    post_list = Article.objects.filter(user__in=subscriptions)\
                                .order_by('-pub_date')
    subscriptions_name = ', '.join([user.username for user in subscriptions])
    followers_list = get_followers(request.user.id)
    context = {
        'post_list': post_list,
        'user': request.user,
        'followers_list': followers_list,
        'subscriptions': subscriptions_name,
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
        send_alert(request.user, a)
        return HttpResponseRedirect(reverse('main:index', args=()))
    else:
        return HttpResponse('Something went wrong')

def get_followers(user_id):
    users = []
    for user in User.objects.all():
        if str(user_id) in user.subscriber.subscribe_list:
            users.append(user)
    return users

def send_alert(author, article):
    followers = get_followers(author.id)
    subject = 'The article is added: "{0}"'.format(article.header)
    from_email = 'info@ti-tech.ru'
    # to = 'ptaiga@gmail.com'
    with mail.get_connection() as connection:
        for user in followers:
            body = '{0}, you received this email '\
                    'because the article "{1}" is added by {2}. '\
                    'Link - http://localhost:8000/main/{3}'\
                    .format(user.first_name, 
                        article.header, 
                        author.username,
                        article.id)
            to = user.email
            mail.EmailMessage(subject, body, from_email, [to],
                                connection=connection).send()

def subscriptions(request):
    subscribe_list = request.user.subscriber.subscribe_list.split(',')
    if (subscribe_list == ['']): subscribe_list = []
    subscriptions = User.objects.filter(id__in = subscribe_list)
    users = User.objects.all().exclude(id__in = subscribe_list)
    context = {
        'users': users,
        'subscriptions': subscriptions,
        'user': request.user,
    }
    return render(request, 'main/subscriptions.html', context)

def subscribe(request):
    if (request.method == 'POST'):
        subscriber = request.user.subscriber
        subscribe = []
        keys = request.POST
        for key in keys:
            if (key[0:4] == 'user'):
                subscribe.append(keys[key])
        #subscribe_list = ','.join(subscribe)
        #return HttpResponse(user.subscriber.subscribe_list + ' -> ' + subscribe_list)   
        subscriber.subscribe_list = ','.join(subscribe)
        subscriber.save()
        return HttpResponseRedirect(reverse('main:index', args=()))
    else:
        return HttpResponse('Something went wrong')


def users(request):
    user_list = User.objects.all()
    return render(request, 'main/users.html', {'user_list': user_list})
    #output = ', '.join([u.username + ': ' + str(u.pk) for u in user_list])
    #return HttpResponse(output)

def send_mail(request):
    subject = 'Test email'
    body = 'This is the test email.'
    from_email = 'info@ti-tech.ru'
    to = 'ptaiga@gmail.com'
    with mail.get_connection() as connection:
        mail.EmailMessage(subject, body, from_email, [to],
                          connection=connection).send()
    return HttpResponse('Sent!')