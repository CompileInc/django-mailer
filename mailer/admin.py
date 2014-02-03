import smtplib
import logging

from socket import error as socket_error

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mailer.models import Message, DontSendEntry, MessageLog

try:
    # Django 1.2
    from django.core.mail import get_connection
except ImportError:
    # ImportError: cannot import name get_connection
    from django.core.mail import SMTPConnection
    get_connection = lambda backend=None, fail_silently=False, **kwds: SMTPConnection(fail_silently=fail_silently)

EMAIL_BACKEND = getattr(settings, "MAILER_EMAIL_BACKEND",
                        "django.core.mail.backends.smtp.EmailBackend")

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "to_addresses", "subject", "when_added", "priority", "email_preview_link"]

    def email_preview_link(self, obj):
        return "<a href='%s' target='_blank'>Preview</a>" % (reverse('mailer_message_detail', args=[obj.id]))
    email_preview_link.short_description = 'Email Preview'
    email_preview_link.allow_tags = True
    actions = ['send_deferred_emails', ]

    def send_deferred_emails(self, request, queryset):
        final_emails = []
        sent = 0
        deferred = 0

        for message in queryset:
            connection = None
            try:
                if connection is None:
                    connection = get_connection(backend=EMAIL_BACKEND)
                logging.info("sending message '%s' to %s" % (message.subject.encode("utf-8"), u", ".join(message.to_addresses).encode("utf-8")))
                email = message.email
                email.connection = connection
                email.send()
                MessageLog.objects.log(message, 1) # @@@ avoid using literal result code
                message.delete()
                sent += 1
            except (socket_error, smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused, smtplib.SMTPAuthenticationError), err:
                message.defer()
                logging.info("message deferred due to failure: %s" % err)
                messages.error(request, "message deferred due to failure: %s" % err)
                MessageLog.objects.log(message, 3, log_message=str(err)) # @@@ avoid using literal result code
                deferred += 1
                # Get new connection, it case the connection itself has an error.
                connection = None

    send_deferred_emails.short_description = _('Send Deferred Emails')


class DontSendEntryAdmin(admin.ModelAdmin):
    list_display = ["to_address", "when_added"]


class MessageLogAdmin(admin.ModelAdmin):
    list_display = ["id", "to_addresses", "subject", "when_attempted", "result", "email_preview_link"]

    def email_preview_link(self, obj):
        return "<a href='%s' target='_blank'>Preview</a>" % (reverse('mailer_message_log_detail', args=[obj.id]))
    email_preview_link.short_description = 'Email Preview'
    email_preview_link.allow_tags = True

admin.site.register(Message, MessageAdmin)
admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)