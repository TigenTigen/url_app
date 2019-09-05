from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from core.models import URL
from core.forms import URLForm

class URLListView(ListView):
    model = URL

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({'form': URLForm()})
        return context

class URLCreateView(CreateView):
    form_class = URLForm
    success_url = reverse_lazy('core:url_list')

def update(request, pk):
    url = get_object_or_404(URL, pk=pk)
    url.delay_and_make_request(now = True)
    return redirect('core:url_list')
