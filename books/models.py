from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    image = models.ImageField(default='default-book.png', upload_to='books/')
    isbn = models.CharField(max_length = 17)

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.book} {self.user}"
