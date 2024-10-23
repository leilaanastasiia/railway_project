import random
import string

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def generate_wagon_number(sender, instance, **kwargs):
    wagon_models = {'CoupeWagon', 'PlatzWagon', 'SVWagon', 'SittingWagon', 'TankWagon'}

    if sender.__name__ in wagon_models and not instance.number:
        while True:
            new_number = ''.join(random.choices(string.digits, k=6))
            if not sender.objects.filter(number=new_number).exists():
                instance.number = new_number
                break