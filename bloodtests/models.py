from django.core.exceptions import ValidationError
from django.db import models


class Test(models.Model):
    __test__ = False
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    upper = models.SmallIntegerField(null=True, blank=True)
    lower = models.SmallIntegerField(null=True, blank=True)

    @property
    def ideal_range(self):
        if not self.lower and not self.upper:
            return f'incalculable'
        if self.lower and self.upper:
            return f'{float(self.lower)} <= value <= {float(self.upper)}'
        if not self.lower:
            return f'value <= {float(self.upper)}'
        if not self.upper:
            return f'value >= {float(self.lower)}'
        return 'incalculable'

    def clean(self):
        if not self.lower and not self.upper:
            raise ValidationError("Lower and upper cannot both be null")
        if self.upper and self.upper < (self.lower or 0):
            raise ValidationError("Lower value can't exceed upper value")
