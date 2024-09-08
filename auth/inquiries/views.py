from django.forms import BaseModelForm
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from inquiries.models import AdministrativeRequests,AcademicRequests

# Administrative Requests views

class AdministrativeRequestsCreateView(CreateView):
    
    model = AdministrativeRequests
    fields = ['subject','body','receiver','reply']
    template_name = 'inquiries/admin_requests_details.html'

    def form_valid(self,form):
        # Attach the current request to the form instance before saving
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('administrativerequests-list')
    
    """
    Adds a table title to the context by calling the Parent's class get.context_data
    and extending it
    Parent class in this case is CreateView 
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Add New Administrative Request' 
        return context
    
    def get_form(self,form_class=None):
        form = super().get_form(form_class)

        # Check if the user is a student
        if self.request.user.is_student():
            # Make the reply's field read-only for students so that field can still be submmitted
            form.fields['reply'].widget.attrs['readonly'] = True
        
        return form

class AdministrativeRequestsUpdateView(UpdateView):
    
    model = AdministrativeRequests
    fields = ['subject','body','receiver','reply']
    template_name = 'inquiries/admin_requests_details.html'

    def get_success_url(self) -> str:
        return reverse_lazy('administrativerequests-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Update Administrative Request'
        return context
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
    
        #Check if the user is student
        if self.request.user.is_student():
            # Make the reply's field read-only for students so that field can still be submmitted
            form.fields['reply'].widget.attrs['readonly'] = True
        
        return form

class AdmininstrativeRequestsListView(ListView):
    
    model = AdministrativeRequests

    # The context object name that will be used in the templates to query the administrative requests
    context_object_name = 'administrative_requests'
    template_name = 'inquiries/admin_requests_list.html'
    paginate_by = 5

    def get_queryset(self):
        
        # Get the currently logged-in user
        user = self.request.user
        
        # If the user is a facilitator, filter administrative requests sent by all students
        if user.is_facilitator():
            return AdministrativeRequests.objects.filter(sender = user)
        
        # If the user is a student, filter administrative requests sent by the student
        elif user.is_student():
            return AdministrativeRequests.objects.filter(sender = user)
    
        # If the user is team lead, return all administrative requests
        elif user.is_teamlead():
            return AdministrativeRequests.objects.all()

class AdministrativeRequestsDeleteView(DeleteView):
    
    model = AdministrativeRequests
    template_name = 'inquiries/confirm-delete.html'

    def get_success_url(self):
        return reverse_lazy('administrativerequests-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Administrative Request' 
        
        # Retrieves the subject of the administrativerequest we want to delete
        administration_request_subject = AdministrativeRequests.objects.get(pk = self.kwargs.get('pk')).subject
        context['delete-confirm-message'] = f'Are you sure yo want to delete this Administrative Request:"{administration_request_subject}"?'

        # Display a cancel button on confirmation page and if pressed , return the user to the academicrequests list 
        context['cancel-url'] = 'administrativerequests-list'
        return context
        
#-------------------------------------------------------------------------------------------------------------------------------        

    
    
