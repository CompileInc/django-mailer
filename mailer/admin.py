from django.contrib import admin
from django.core.urlresolvers import reverse

from mailer.models import Message, DontSendEntry, MessageLog


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "to_addresses", "subject", "when_added", "priority", "email_preview_link"]

    def email_preview_link(self, obj):
        return "<a href='%s' target='_blank'>Preview</a>" % (reverse('mailer_message_detail', args=[obj.id]))
    email_preview_link.short_description = 'Email Preview'
    email_preview_link.allow_tags = True


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