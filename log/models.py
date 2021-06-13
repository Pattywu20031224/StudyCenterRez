from seat.models import Seat
from django.db.models import *
from seat.models import *
from user.models import *

# Create your models here.
# 借閱紀錄
class Log(Model):
    
    #user = ForeignKey(User, CASCADE)
    equip = ForeignKey(Seat, CASCADE)
    checkout = DateTimeField('借用時間', auto_now_add=True)
    returned = DateTimeField('歸還時間', null=True)    # 以 null 代表尚未歸還

    def __str__(self):
        return "{} | {} | {}".format(
            self.checkout, 
            self.user.realname, 
            self.seat.SerialNumber
        )
