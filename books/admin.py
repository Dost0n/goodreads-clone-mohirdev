from django.contrib import admin
from books.models import Book, Author, BookAuthor, BookReview
from django.contrib.auth.models import Group


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    # list_filter = ('title')
    list_display = ('title', 'isbn', 'description')


admin.site.unregister(Group)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(BookAuthor)
admin.site.register(BookReview)