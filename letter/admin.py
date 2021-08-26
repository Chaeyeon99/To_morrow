from django.contrib import admin
from letter.models import Letter, Receiveletter, Sendletter

class LetterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'content', 'senderId', 'sendDate' )
    list_filter = ('emotion', )

    fieldsets = (
        ('Letter', {'fields': ('content', 'emotion')}),
        ('Letter info', {'fields': ('receiveDate',)}),
    )
    exclude = ('sendDate',)
    search_fields = ('content',)
    ordering = ('sendDate',)


admin.site.register(Letter,LetterAdmin)


class ReceiveletterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'receiverId', 'is_deleted', 'readCheck' )
    list_filter = ('is_deleted', 'readCheck' )

    fieldsets = (
        ('Letter info', {'fields': ('receiverId',)}),
        ('Letter status', {'fields': ('is_deleted', 'readCheck')}),
    )
    ordering = ('receiveCol',)


admin.site.register(Receiveletter,ReceiveletterAdmin)


class SendletterAdmin(admin.ModelAdmin):
    list_display = ('letterId', 'senderId', 'is_deleted' )
    list_filter = ('is_deleted', )

    fieldsets = (
        ('Letter info', {'fields': ('letterId', 'senderId')}),
        ('Letter status', {'fields': ('is_deleted',)}),
    )
    ordering = ('sendCol',)


admin.site.register(Sendletter,SendletterAdmin)
