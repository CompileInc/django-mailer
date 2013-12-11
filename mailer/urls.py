from django.conf.urls import *

from mailer.views import view_message, view_message_log

urlpatterns = patterns('mailer.views',
        url('^preview_message/(?P<id>\d+)/$', view_message,
            name='mailer_message_detail'),
        url('^preview_message_log/(?P<id>\d+)/$', view_message_log,
            name='mailer_message_log_detail'),
        )
