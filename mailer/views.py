from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from mailer.models import Message, MessageLog


def get_html_from_email(email):
    if hasattr(email, 'alternatives'):
        html = filter(lambda x:x[1]=='text/html', email.alternatives)
        if len(html) > 0:
            return (True, html[0][0])
    return (False, email.body)


@staff_member_required 
def view_message(request, id):
    message = get_object_or_404(Message, id=id)
    success, html = get_html_from_email(message.email)
    content_type="text/html"
    if not success:
        content_type="text/plain"
    return HttpResponse(html, content_type=content_type)


@staff_member_required
def view_message_log(request, id):
    message_log = get_object_or_404(MessageLog, id=id)
    success, html = get_html_from_email(message_log.email)
    content_type="text/html"
    if not success:
        content_type="text/plain"
    return HttpResponse(html, content_type=content_type)
