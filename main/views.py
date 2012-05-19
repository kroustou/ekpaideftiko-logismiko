#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
import forms


class RegistrationView(FormView):
    form_class = forms.NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_staff = form.cleaned_data['is_staff']
        obj.first_name = form.cleaned_data['first_name']
        obj.last_name = form.cleaned_data['last_name']
        obj.save()
        return super(RegistrationView, self).form_valid(self)


def main(request):
    user = request.user
    return render_to_response('front-page.html', {'user': user})
