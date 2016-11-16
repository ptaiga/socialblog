from django.core import mail

from django.contrib.auth.models import User

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