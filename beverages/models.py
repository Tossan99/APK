from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Beverage(models.Model):
    """
    Model for beverages
    """
    category = models.ForeignKey('Category', null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    volume = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)], blank=False) #Volume in ml
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False) #Price in sek
    percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=False) #Alcohol percentage

    def __str__(self):
        return self.name
    
    @property
    def calculate_apk(self):
        """
        Calculates the beverage apk, how many ml of 40% alcoholic liquid for each sek
        """
        apk = ((self.percentage / 100) * self.volume) / self.price
        return round(apk, 2)
    
    @property
    def calculate_price_per_unit(self):
        """
        Calculates price_per_unit in sek
        One unit is set to 40ml 40% alcohol
        """
        percentage = float(self.percentage) / 100
        hundred_percentage_volume = percentage * float(self.volume)
        forty_percentage_volume = hundred_percentage_volume / 0.4
        standard_units = forty_percentage_volume / 40 #Divided in 40ml to get amount of standard units
        price_per_unit = float(self.price) / standard_units
        return round(price_per_unit, 2)
        
        