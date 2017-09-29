from __future__ import unicode_literals

from django.db import models

class LegoProduct(models.Model):
    product_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    product_code = models.IntegerField(db_index=True)
    piece_count = models.IntegerField()
    datetime_updated = models.DateTimeField('datetime updated', auto_now_add=True)

    def __unicode__(self):
        return '{code}: {title}'.format(
            code = self.product_code,
            title = self.title,
        )

class LegoProductImage(models.Model):
    lego_product = models.ForeignKey('LegoProduct')
    img_url = models.TextField()

    def __unicode__(self):
        return '{prod} - {url}'.format(
            prod = unicode(self.lego_product),
            url = self.img_url,
        )

class LegoProductSku(models.Model):
    lego_product = models.ForeignKey('LegoProduct')
    site = models.CharField(max_length=255)
    sku_number = models.CharField(max_length=40)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=3)
    product_url = models.TextField()
    datetime_updated = models.DateTimeField('datetime updated', auto_now_add=True)

    class Meta:
        unique_together = (
            ( "lego_product", "site", "sku_number" ),
        )

    def __unicode__(self):
        return '{prod} - {sku} @ {site}'.format(
            prod = unicode(self.lego_product),
            sku = self.sku_number,
            site = self.site,
        )

    
