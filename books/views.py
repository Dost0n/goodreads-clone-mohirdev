from django.shortcuts import render, redirect
from books.models import Book, BookReview
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from books.forms import ReviewCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from django.contrib import messages

class BooksView(ListView):
    template_name = 'book_list.html'
    queryset = Book.objects.all().order_by("id")
    context_object_name = 'books'
    paginate_by = 2



class bookDetailView(DetailView):
    template_name = 'book-detail.html'
    queryset = Book.objects.all()
    pk_url_kwarg = 'id'



def book_list(request):
    books = Book.objects.all().order_by("id")
    search_query = request.GET.get('q', "")
    if search_query:
        books = books.filter(title__icontains = search_query)
    page_size = request.GET.get('page_size', 2)
    paginator = Paginator(books, page_size)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    if page_obj:
        context = {
            'page_obj':page_obj,
            'search_query':search_query
        }
        return render(request, 'book_list.html', context)
    else:
        return HttpResponse("<h1>No books</h1>")


def book_detail(request, id):
    book = Book.objects.get(id=id)
    form = ReviewCreateForm(instance=request.user)
    context = {
        'book':book,
        'form':form
    }
    return render(request, 'book-detail.html', context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = ReviewCreateForm(data = request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user = request.user,
                stars_given = review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:book_detail', kwargs={"id":book.id}))
        context = {
            "book":book,
            "review_form":review_form
        }
        return render(request, 'book-detail.html', context)
    

class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = ReviewCreateForm(instance=review)
        context = {
            'book': book,
            'review':review,
            'review_form':review_form
        }
        return render(request, 'edit-review.html', context)
    
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = ReviewCreateForm(instance=review, data=request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:book_detail', kwargs={"id":book.id}))
        else:
            context = {
                'book': book,
                'review':review,
                'review_form':review_form
            }
            return render(request, 'edit-review.html', context)
        
        


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = ReviewCreateForm(instance=review)
        context = {
            'book': book,
            'review':review,
            'review_form':review_form
        }
        return render(request, 'delete-review.html', context)
        
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review.delete()
        messages.success(request, 'You successfully deleted this view')
        return redirect(reverse('books:book_detail' , kwargs={"id":book.id}))