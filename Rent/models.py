from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        abstract = True


class Car(BaseModel):
    type_engines = {
        ('Petrol', 'Benzyna'),
        ('Diesel', 'Diesel'),
        ('Hybrid', 'Hybryda'),
        ('Electric', 'Elektryczny')
    }
    type_transmission = {
        ('Automatic', 'Automatyczna'),
        ('Manual', 'Manualna')
    }
    type_drives = {
        ('FWD', 'Przedni'),
        ('RWD', 'Tylni'),
        ('AWD', '4x4')
    }
    type_car = {
        ('Kombi', 'Kombi'),
        ('Sedan', 'Sedan'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('Suv', 'Suv'),
        ('Van', 'Van')
    }

    brand = models.CharField(max_length=32, unique=True)
    model = models.CharField(max_length=32)
    cars_type = models.CharField(max_length=32, choices=type_car)
    engine = models.CharField(max_length=16, choices=type_engines)
    capacity = models.FloatField()
    year = models.CharField(max_length=4)
    number_of_seats = models.IntegerField()
    Consumption = models.CharField(max_length=16)
    power = models.CharField(max_length=4)
    car_mileage = models.CharField(max_length=7)
    transmission = models.CharField(max_length=32, choices=type_transmission)
    drive = models.CharField(max_length=32, choices=type_drives)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.brand}, {self.model}"


class CompanyBranches(BaseModel):
    city = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self


class Client(BaseModel):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=256, unique=True)
    phone = models.CharField(max_length=32)
    driving_license_no = models.CharField(max_length=32)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self


class Rent(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    period = models.IntegerField(default=0)
    take_from = models.ForeignKey(CompanyBranches, related_name='rents_taken', on_delete=models.CASCADE)
    take_back = models.ForeignKey(CompanyBranches, related_name='rents_returned', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Obliczanie wartości pola 'period' na podstawie różnicy między 'start_date' a 'end_date'
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.period = delta.days

        # Obliczanie wartości pola 'amount' na podstawie ceny samochodu i okresu wynajmu
        if self.car and self.period:
            self.amount = self.car.price * self.period

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rent of {self.car} by {self.client}"


