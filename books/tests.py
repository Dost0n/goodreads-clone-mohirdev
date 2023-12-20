from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview, Author, BookAuthor
from users.models import CustomUser


class BooksTestCase(TestCase):

    # test1
    def test_no_books(self):
        response = self.client.get(reverse('books:book-list'))

        self.assertContains(response, "No books")

    # test2
    def test_books_list(self):
        book1 = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        book2 = Book.objects.create(title = "Book2",description = "Description2",isbn = "123467")
        book3 = Book.objects.create(title = "Book3",description = "Description3",isbn = "123478")

        response = self.client.get(reverse('books:book-list')+"?page_size=2")


        for book in [book1, book2]:
            self.assertContains(response, book.title)
        
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books:book-list')+"?page=2&page_size=2")
        self.assertContains(response, book3.title)
    
    # test3
    def test_detail_page(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        author = Author.objects.create(first_name = "Doston", last_name = "Imomaliyev", email = "ctron1108@gmail.com", description = "description1")
        bookauthor = BookAuthor.objects.create(book = book, author = author)
        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        
        self.client.login(username='doston', password='doston123')

        response = self.client.get(reverse('books:book_detail', kwargs={"id":book.id}))
        self.assertContains(response, bookauthor.author.full_name)
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
    
    # test4
    def test_search_books(self):
        book1 = Book.objects.create(title = "Sport",description = "Description1",isbn = "123456")
        book2 = Book.objects.create(title = "Guide",description = "Description2",isbn = "123467")
        book3 = Book.objects.create(title = "Shoe Dog",description = "Description3",isbn = "123478")

        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        self.client.login(username='doston', password='doston123')

        response = self.client.get(reverse('books:book-list')+"?q=sport")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:book-list')+"?q=guide")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books:book-list')+"?q=shoe")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

        response = self.client.get(reverse('books:book-list')+"?q=technology")

        self.assertContains(response, "No books")
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)



class BooksReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title = "Sport",description = "Description1",isbn = "123456")


        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        self.client.login(username='doston', password='doston123')

        self.client.post(reverse("books:book_review", kwargs={"id":book.id}),
                         data={
                            "stars_given":3,
                            "comment":"Nice book"
                        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
