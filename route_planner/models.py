from django.db import models
from django_extensions.db.models import TimeStampedModel



class TruckStop(TimeStampedModel):
    truckstop_name = models.CharField(
        max_length=255,
        verbose_name="Truck Stop Name",
        help_text="Name of the truck stop or fuel station"
    )

    address = models.CharField(
        max_length=500,
        verbose_name="Address",
        help_text="Full street address of the truck stop"
    )

    city = models.CharField(
        max_length=100,
        verbose_name="City",
        help_text="City where truck stop is located"
    )

    state = models.CharField(
        max_length=10,
        verbose_name="State",
        help_text="State abbreviation (e.g. TX, CA)"
    )

    rack_id = models.IntegerField(
        verbose_name="Rack ID",
        help_text="Fuel rack identifier for pricing source"
    )

    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name="Retail Price",
        help_text="Current retail fuel price"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Record creation timestamp"
    )

    class Meta:
        verbose_name = "Truck Stop"
        verbose_name_plural = "Truck Stops"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'truckstop_name',
                    'address',
                    'city',
                    'state',
                    'rack_id',
                    'retail_price',
                ],
                name='unique_truckstop_full_record'
            )
        ]

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"