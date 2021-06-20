from django.db.models import *


class Seat(Model):
    SerialNumber = CharField('座位編號', max_length=255)
    test = 0
    def __str__(self):
        return "{}".format(self.SerialNumber)

