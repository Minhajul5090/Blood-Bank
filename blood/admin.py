from django.contrib import admin
from . import models

@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['bloodgroup', 'unit']
    list_filter = ['bloodgroup']
    search_fields = ['bloodgroup']

@admin.register(models.BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'bloodgroup', 'unit', 'status', 'date', 'accepted_by_donor']
    list_filter = ['status', 'bloodgroup', 'date']
    search_fields = ['patient_name', 'reason']
    readonly_fields = ['date', 'accepted_by_donor']
    actions = ['forward_to_donors', 'approve_requests', 'reject_requests']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('patient_name', 'patient_age', 'reason', 'bloodgroup', 'unit')
        }),
        ('Request Details', {
            'fields': ('request_by_patient', 'request_by_donor', 'status', 'date')
        }),
        ('Donor Response', {
            'fields': ('accepted_by_donor', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def forward_to_donors(self, request, queryset):
        """Custom action to forward requests to donors"""
        count = 0
        for blood_request in queryset.filter(status='Pending'):
            if blood_request.forward_to_donors():
                count += 1
        
        if count == 1:
            message = f"{count} request was forwarded to donors."
        else:
            message = f"{count} requests were forwarded to donors."
        
        self.message_user(request, message)
    
    forward_to_donors.short_description = "Forward selected requests to donors"
    
    def approve_requests(self, request, queryset):
        """Custom action to approve accepted requests"""
        count = 0
        for blood_request in queryset.filter(status='Accepted'):
            if blood_request.approve_by_admin():
                count += 1
        
        if count == 1:
            message = f"{count} request was approved."
        else:
            message = f"{count} requests were approved."
        
        self.message_user(request, message)
    
    approve_requests.short_description = "Approve selected accepted requests"
    
    def reject_requests(self, request, queryset):
        """Custom action to reject requests"""
        updated = queryset.update(status='Rejected')
        if updated == 1:
            message = f"{updated} request was rejected."
        else:
            message = f"{updated} requests were rejected."
        
        self.message_user(request, message)
    
    reject_requests.short_description = "Reject selected requests"
    
    def get_queryset(self, request):
        """Custom queryset to show donor requests count"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('donor_requests')

@admin.register(models.DonorRequest)
class DonorRequestAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_request', 'status', 'response_date']
    list_filter = ['status', 'response_date', 'blood_request__bloodgroup']
    search_fields = ['donor__user__first_name', 'donor__user__last_name', 'blood_request__patient_name']
    readonly_fields = ['response_date']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('blood_request', 'donor')
        }),
        ('Response Details', {
            'fields': ('status', 'response_date', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        """Custom queryset to optimize database queries"""
        qs = super().get_queryset(request)
        return qs.select_related('donor__user', 'blood_request')
