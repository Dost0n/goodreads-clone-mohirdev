from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    
    def test_paginated_list(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")

        user =  CustomUser.objects.create(
                                    username = "doston",
                                    last_name = "Imomaliyev",
                                    first_name = "Doston",
                                    email = "ctron1108@gmail.com"
                                )
        user.set_password('doston123')
        user.save()

        review1=BookReview.objects.create(book = book, user = user, stars_given = 3, comment = "Description1")
        review2=BookReview.objects.create(book = book, user = user, stars_given = 4, comment = "Description2")
        review3=BookReview.objects.create(book = book, user = user, stars_given = 5, comment = "Description3")


        response = self.client.get(reverse('home')+"?page_size=2")

        self.assertNotContains(response, review1.comment)
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)