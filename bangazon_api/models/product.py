from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(
        "Store", on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=7, validators=[
                                MinValueValidator(0.00), MaxValueValidator(10000.00)])
    description = models.TextField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=100)
    image_path = models.ImageField(upload_to='products', height_field=None,
                                   width_field=None, max_length=None, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name='products')

    @property
    def average_rating(self):
        """Average rating calculated attribute for each product
        Returns:
            number -- The average rating for the product
        """
        # total_rating = 0
        # for rating in self.ratings:
        #     total_rating += rating.rating

        # avg = total_rating / len(self.ratings)
        # return avg
