from django.contrib import admin
from letter.models import Letter, Receiveletter, Sendletter

class LetterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'content', 'senderId', 'sendDate' )
    list_filter = ('emotion', )

    fieldsets = (
        ('Letter info', {'fields': ('content', 'emotion')}),
        ('Letter info', {'fields': ('receiveDate',)}),
    )
    exclude = ('sendDate',)
    search_fields = ('content',)
    ordering = ('sendDate',)


admin.site.register(Letter,LetterAdmin)


class ReceiveletterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'content', 'receiverId', 'sendDate' )
    list_filter = ('emotion', )

    fieldsets = (
        ('Letter info', {'fields': ('content', 'emotion')}),
        ('Letter info', {'fields': ('receiveDate',)}),
    )
    exclude = ('sendDate',)
    search_fields = ('content',)
    ordering = ('sendDate',)


admin.site.register(Receiveletter,ReceiveletterAdmin)

class SendletterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'content', 'senderId', 'sendDate' )
    list_filter = ('emotion', )

    fieldsets = (
        ('Letter info', {'fields': ('content', 'emotion')}),
        ('Letter info', {'fields': ('receiveDate',)}),
    )
    exclude = ('sendDate',)
    search_fields = ('content',)
    ordering = ('sendDate',)


admin.site.register(Sendletter,SendletterAdmin)