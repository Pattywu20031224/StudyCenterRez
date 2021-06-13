from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from log.models import Log


# Create your views here.
class SeatList(LoginRequiredMixin, ListView):   
    model = Seat    
    paginate_by = 10

class SeatView(LoginRequiredMixin, DetailView):
    model = Seat
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['log_list'] = Log.objects.filter(
            equip=self.object, 
        ).order_by('-id').select_related('user')
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