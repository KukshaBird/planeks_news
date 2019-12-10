from celery import Celery
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from planeks_auth.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@shared_task
def celey_send_mail(user, current_site, form):
    mail_subject = 'Активируйте свою учетную запись.'
    message = render_to_string('planeks_auth/address_confirm_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()

@shared_task
def new_comment_email(post):
    mail_subject = 'Новый комментарий'
    message = render_to_string('news/new_comment_email.html', {
        'post': post,
    })
    to_email = post.author.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()