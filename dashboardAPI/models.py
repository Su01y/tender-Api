from django.db import models
from .category import categorize


class Purchases(models.Model):
    pusch_id = models.CharField(max_length=32, primary_key=True)
    purchase_name = models.CharField(max_length=256)
    lot_name = models.CharField(max_length=256)
    price = models.FloatField()
    customer_inn = models.IntegerField()
    customer_name = models.CharField(max_length=256)
    delivery_region = models.CharField(max_length=256)
    publish_date = models.DateTimeField()
    contract_category = models.CharField(max_length=256)
    category = models.CharField(max_length=256, blank=True, null=True)

    def save(self, *args, **kwargs):
        cat = categorize(self.lot_name)
        if cat:
            self.category = cat
        print(self.category)
        super(Purchases, self).save(*args, **kwargs)


class Companies(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True, serialize=True)
    name = models.CharField(max_length=256)
    supplier_inn = models.IntegerField()
    supplier_kpp = models.CharField(max_length=256)
    okved = models.CharField(max_length=256)
    status = models.BooleanField()
    count_managers = models.IntegerField()


class Participants(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    purch_id = models.CharField(max_length=32)
    supplier_inn = models.IntegerField()
    is_winner = models.CharField(max_length=255)


class Contracts(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    purch_id = models.CharField(max_length=256)
    contract_reg_number = models.CharField(default=None, max_length=256, null=True, blank=True)
    price = models.FloatField()
    contract_conclusion_date = models.DateTimeField()    