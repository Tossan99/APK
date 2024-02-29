from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from cloudinary.models import CloudinaryField

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
    #image = models.URLField(max_length=1024, null=True, blank=True, default='placeholder')
    volume = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)], blank=False) #Volume in ml
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False) #Price in sek
    percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=False) #Alcohol percentage
    apk = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0) #Price in sek

    def __str__(self):
        return self.name
    
    def _calculate_apk(self):
        """
        Calculates the beverage apk, how many ml of 40% alcoholic liquid for each sek
        """
        apk = ((self.percentage / 100) * self.volume) / self.price
        return round(apk, 2)
    
    def _calculate_price_per_unit(self):
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
        

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the apk and price_per_unit.
        """
        self.apk = self._calculate_apk()
        self.price_per_unit = self._calculate_price_per_unit()
        super().save(*args, **kwargs)