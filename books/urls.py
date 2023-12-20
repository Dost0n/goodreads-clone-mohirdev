from django.urls import path
from books.views import  BooksView, bookDetailView, book_list, book_detail, AddReviewView, EditReviewView, DeleteReviewView


app_name = 'books'
urlpatterns = [
    path('', book_list, name='book-list'),
    path('<int:id>/', book_detail, name='book_detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='book_review'),
    path('<int:book_id>/review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('<int:book_id>/review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]