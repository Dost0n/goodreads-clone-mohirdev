from rest_framework.test import APITestCase
from users.models import CustomUser
from books.models import Book, BookReview
from rest_framework.reverse import reverse

class HomePageTestCase(APITestCase):

    def setUp(self):
        self.user =  CustomUser.objects.create(username = "doston",first_name = "Doston", last_name = "Imomaliyev",email = "ctron1108@gmail.com")
        self.user.set_password('doston123')
        self.user.save()
        self.client.login(username='doston', password='doston123')

    def test_book_review_detail(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        review = BookReview.objects.create(book = book, user = self.user, stars_given = 5, comment = "Very good book")

        response = self.client.get(reverse('api:review-detail', kwargs = {'id': review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], review.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], "Book1")
        self.assertEqual(response.data['book']['description'], "Description1")
        self.assertEqual(response.data['book']['isbn'], "123456")
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], "Doston")
        self.assertEqual(response.data['user']['last_name'], "Imomaliyev")
        self.assertEqual(response.data['user']['email'], "ctron1108@gmail.com")
        self.assertEqual(response.data['user']['username'], "doston")
    

    def test_delete_review(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        review = BookReview.objects.create(book = book, user = self.user, stars_given = 5, comment = "Very good book")

        response = self.client.delete(reverse('api:review-detail', kwargs = {'id': review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=review.id).exists())


    def test_patch_review(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        review = BookReview.objects.create(book = book, user = self.user, stars_given = 5, comment = "Very good book")

        response = self.client.patch(reverse('api:review-detail', kwargs = {'id': review.id}), data = {'stars_given':4})
        review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.stars_given, 4)


    def test_put_review(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        review = BookReview.objects.create(book = book, user = self.user, stars_given = 5, comment = "Very good book")

        response = self.client.patch(reverse('api:review-detail', kwargs = {'id': review.id}), data = {'stars_given':4, "comment":"Very very very good book"})
        review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.stars_given, 4)
        self.assertEqual(review.comment, "Very very very good book")

    def test_create_review(self):
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        data = {
            'stars_given':2,
            "comment":"bad book",
            "user_id" : self.user.id,
            "book_id": book.id
        }
        response = self.client.post(reverse('api:book-review-list'), data=data)
        review = BookReview.objects.get(book = book)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(review.stars_given, 2)
        self.assertEqual(review.comment, "bad book")

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username = "w1zard", first_name = "w1zard")
        book = Book.objects.create(title = "Book1",description = "Description1",isbn = "123456")
        review1 = BookReview.objects.create(id=1, book = book, user = self.user, stars_given = 5, comment = "Very good book")
        review2 = BookReview.objects.create(id=2, book = book, user = user_two, stars_given = 4, comment = "Not good book")

        response = self.client.get(reverse('api:book-review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][1]['id'], review2.id)
        self.assertEqual(response.data['results'][1]['stars_given'], review2.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], review2.comment)
        self.assertEqual(response.data['results'][0]['id'], review1.id)
        self.assertEqual(response.data['results'][0]['stars_given'], review1.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], review1.comment)
