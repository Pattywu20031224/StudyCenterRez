from django.db.models.expressions import OuterRef, Subquery
from django.urls import reverse,reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, datetime
from django.contrib.auth.models import User, Group
from django.views.generic.dates import DateMixin
from seat.models import Seat
from .models import Log
from django.utils import timezone
from datetime import timedelta, datetime


# 借閱記錄列表
class LogList(LoginRequiredMixin, ListView):
    model = Log
    ordering = ['-checkout']
    paginate_by = 20
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        delta = timedelta(days=1)
        today = timezone.localdate()
        options = []
        for i in range(7):
            today += delta
            options.append(today)
        ctx['option_list'] = options
        ctx['qdate'] = date.today
        return ctx
    


class CheckoutUser(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 20
    template_name = 'log/checkout_user_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            users = User.objects.filter(username__icontains=query)
        else:
            users = User.objects
        return users.order_by('username')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('query') or ""
        return ctx

class CheckoutSeat(LoginRequiredMixin, ListView):
    model = Seat
    paginate_by = 5
    template_name = 'log/checkout_seat_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            seats = Seat.objects.filter(title__icontains=query)
        else:
            seats = Seat.objects
        return seats.exclude(
            log__checkout__isnull=False, 
            log__returned__isnull=True
        ).order_by('SerialNumber')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        curr_user = User.objects.get(id=self.kwargs['rid'])
        ctx['query'] = self.request.GET.get('query') or ""
        ctx['user'] = curr_user
        ctx['borrowing'] = curr_user.log_set.filter(
            returned__isnull=True
        ).select_related('seat')
        return ctx

class CheckoutLog(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        user = User.objects.get(id=self.kwargs['rid'])
        seat = Seat.objects.get(id=self.kwargs['bid'])
        log = Log(user=user, seat=seat)
        log.save()
        return reverse('checkout_seat', kwargs={'rid': user.id})

class ReturnSeat(LoginRequiredMixin, ListView):
    model = Log
    paginate_by = 20
    template_name = 'log/return_seat_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            logs = Log.objects.filter(seat__SerialNumber=query)
        else:
            logs = Log.objects
        return logs.exclude(
            returned__isnull=False
        ).select_related('seat', 'user')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('query') or ""
        return ctx
class ReturnLog(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        log = Log.objects.get(id=self.kwargs['lid'])
        log.returned = datetime.now()
        log.save()
        return reverse('log_list')

class LogDelete(LoginRequiredMixin, DeleteView):
    model = Log
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('log_list')
