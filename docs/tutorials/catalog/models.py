from django.db import models
from django.utils.translation import ugettext_lazy as _

from north.dbutils import BabelNamed

class Product(BabelNamed):
  
    price = models.DecimalField(_("Price"),blank=True,null=True,decimal_places=2,max_digits=10)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    