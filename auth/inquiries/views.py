from django.db.models.query import QuerySet
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
    
    # reverse returns the string url path
    def get_success_url(self) -> str:
        return reverse_lazy('admin-requests-list')
    
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

    # reverse returns the string url path   
    def get_success_url(self) -> str:
        return reverse_lazy('admin-requests-list')

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
    
        # If the user is teamlead, return all administrative requests
        elif user.is_teamlead():
            return AdministrativeRequests.objects.all()

class AdministrativeRequestsDeleteView(DeleteView):
    
    model = AdministrativeRequests
    template_name = 'inquiries/confirm_delete.html'

    # reverse returns the string url path
    def get_success_url(self):
        return reverse_lazy('admin-requests-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Administrative Request' 
        
        # Retrieves the subject of the administrativerequest we want to delete
        administration_request_subject = AdministrativeRequests.objects.get(pk = self.kwargs.get('pk')).subject
        context['message'] = f'Are you sure yo want to delete this Administrative Request:  "{administration_request_subject}"?'

        # Display a cancel button on confirmation page and if pressed , return the user to the academicrequests list 
        context['cancel_url'] = 'admin-requests-list'
        return context
        
#-------------------------------------------------------------------------------------------------------------------------------        
 
class AcademicRequestsCreateView(CreateView):
    
    model = AcademicRequests
    fields = ['subject', 'body', 'receiver', 'reply']
    template_name = 'inquiries/academic_requests_details.html'


    def form_valid(self, form):
        # Attach the current request to the form instance before saving
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    # reverse returns the string url path
    def get_success_url(self):
        return reverse_lazy('academic-requests-list')

    # Adds a title to the context by calling the Parent's class get_context_data and extending it
    # Parent class in this case is CreateView
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Add new Academic Request' 
        return context
     
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Check is the user is student
        if self.request.user.is_student():
            # Make the 'reply' field read-only so that the field can still be submitted
            form.fields['reply'].widget.attrs['readonly']= True
        
        return form

class AcademicRequestsUpdateView(UpdateView):
    
    model = AcademicRequests
    fields = ['subject','body','receiver','reply']
    template_name = 'inquiries/academic_requests_details.html'

    # reverse returns the string url path
    def get_success_url(self):
        return reverse_lazy('academic-requests-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = 'Update Academic Request'
        return context

    def get_form(self, form_class = None):
        form = super().get_form(form_class)

        # Check if the user is student or teamlead
        if self.request.user.is_student() or self.request.user.is_teamlead():
            # Make the 'reply' field read-only for students and teamleads, so that the
            # field can still be submitted
            form.fields['reply'].widget.attrs['readonly'] = True
            
        return form
                
class AcademicRequestsListView(LoginRequiredMixin,ListView):
    
    model = AcademicRequests

    # The context object name will be used in the templates to query the academic requests
    context_object_name = 'academic_requests'
    template_name = 'inquiries/academic_requests_list.html'
    paginate_by = 5

    def get_queryset(self):
        
        # Get the currently logged-in user
        user = self.request.user
        
        #If the user is facilitator, filter academic requests where the receiver is the facilitator
        if user.is_facilitator():
            return AcademicRequests.objects.filter(receiver = user)

        # If the user is a student, filter academic requests sent by the student
        elif user.is_student():
            return AcademicRequests.objects.filter(sender = user)  

        # If the user is a teamlead, return all academic requests 
        elif user.is_teamlead():
            return AcademicRequests.objects.all()
        
class AcademicRequestsDeleteView(DeleteView):
    
    model = AcademicRequests
    template_name = 'inquiries/confirm_delete.html'

    # reverse returns the string url path
    def get_success_url(self):
        return reverse_lazy('academic-requests-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Academic Request' 
        
        # Retrieves the subject of the academic request we want to delete
        academic_request_subject = AcademicRequests.objects.get(pk =self.kwargs.get('pk')).subject
        context['message'] = f'Are you sure you want to delete this academic request: "{academic_request_subject}" ?'
        # Display a cancel button on confirmation page and if pressed, return user to the academic requests list
        context['cancel_url'] = 'academic-requests-list'
        return context
    
        


















    
