from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from log.models import Log
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User

# Create your views here.
class SeatList(LoginRequiredMixin, ListView):   
    model = Seat

    def get_queryset(self):
        delta = timedelta(days=1)
        today = timezone.localdate()
        if 'rdate' in self.request.POST:
            self.rdate = datetime.fromisoformat(self.request.POST.get('rdate')).date()
        else:
            self.rdate = today + delta
        # annotate 的作用是在查詢組中加入資料模型裡原本沒有的欄位
        return Seat.objects.annotate(
            user = Subquery(
                Log.objects.filter(
                    seat_id=OuterRef('id'), 
                    reserve_date=self.rdate,
                ).values('user__first_name')[:1]
            ),
        )#.filter(user__isnull=True)

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
        ctx['qdate'] = self.rdate
        return ctx

class SeatView(LoginRequiredMixin, DetailView):
    model = Seat
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
class SeatAdd(LoginRequiredMixin, CreateView):  
    model = Seat
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('seat_list')

class SeatEdit(LoginRequiredMixin, UpdateView): 
    model = Seat
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('seat_list')

class EquipDelete(LoginRequiredMixin, DeleteView):   
    model = Seat
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('seat_list')
class SeatReserve(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs) :
        rdate = self.request.GET.get('d')

        Log(
            user=self.request.user,
            seat=Seat.objects.get(id=self.kwargs['pk']),
            reserve_date = datetime.fromisoformat(rdate)
        ).save()
        return reverse('log_list')