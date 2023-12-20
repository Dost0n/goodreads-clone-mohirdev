from django.shortcuts import render
from books.models import BookReview
from django.core.paginator import Paginator


def home(request):
    book_review = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(book_review, page_size)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'landing.html', context)