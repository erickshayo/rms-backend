from django.db import models
# from authUser.models import User

# Create your models here.

class Wilaya(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Kata(models.Model):
    name = models.CharField(max_length=200)
    wilaya_id = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return f'wilaya {self.wilaya_id.name} kata {self.name}'


class Mtaa(models.Model):
    name = models.CharField(max_length=200)
    kata_id = models.ForeignKey(Kata, on_delete=models.CASCADE)

    def __str__(self):
        return f'wilaya {self.kata_id.name} kata {self.name}'


class Citizen(models.Model):
    nida = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100, unique=True)
    lastname = models.CharField(max_length=100, unique=True)
    mtaa = models.ForeignKey(Mtaa, on_delete=models.CASCADE)
    kata = models.ForeignKey(Kata, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    house_no = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    email = models.EmailField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    M = "M"
    F = "F"
    CHOICES = (
        (M, 'Male'),
        (F, "Female")
    )
    gender = models.CharField(max_length=10, choices=CHOICES)

    # class Meta:
    #     ordering = ('-id',)

    def __str__(self):
        return f'{self.firstname}'
