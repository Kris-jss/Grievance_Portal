from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint, Response


@login_required
def student_dashboard(request):
    """Student dashboard - submit and view complaints"""
    
    # Handle complaint submission
    if request.method == 'POST':
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        evidence = request.FILES.get('evidence')
        
        # Create complaint
        complaint = Complaint.objects.create(
            student=request.user,
            category=category,
            subject=subject,
            description=description,
            evidence=evidence
        )
        
        messages.success(request, f"Complaint {complaint.complaint_id} submitted successfully!")
        return redirect('student_dashboard')
    
    # Get user's complaints
    complaints = Complaint.objects.filter(student=request.user)
    
    context = {
        'complaints': complaints,
        'total': complaints.count(),
        'pending': complaints.filter(status='pending').count(),
        'in_progress': complaints.filter(status='in_progress').count(),
        'resolved': complaints.filter(status='resolved').count(),
    }
    return render(request, 'complaints/student_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard - view and respond to all complaints"""
    if request.user.role != 'admin':
        messages.error(request, "Access denied! Admin only.")
        return redirect('student_dashboard')
    
    # Handle admin response
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        response_message = request.POST.get('response_message')
        status = request.POST.get('status')
        
        complaint = get_object_or_404(Complaint, id=complaint_id)
        
        # Create response
        Response.objects.create(
            complaint=complaint,
            responder=request.user,
            message=response_message
        )
        
        # Update complaint status
        complaint.status = status
        complaint.save()
        
        messages.success(request, f"Response added to {complaint.complaint_id} and status updated!")
        return redirect('admin_dashboard')
    
    # Filter complaints by status
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'archived':
        # Show only archived (not deleted)
        complaints = Complaint.objects.filter(archived_by_admin=True, deleted_by_admin=False)
    elif status_filter == 'all':
        # Show active complaints (not archived, not deleted)
        complaints = Complaint.objects.filter(archived_by_admin=False, deleted_by_admin=False)
    else:
        # Show specific status (not archived, not deleted)
        complaints = Complaint.objects.filter(status=status_filter, archived_by_admin=False, deleted_by_admin=False)
    
    all_complaints = Complaint.objects.filter(deleted_by_admin=False)
    
    context = {
        'complaints': complaints,
        'total': all_complaints.filter(archived_by_admin=False).count(),
        'pending': all_complaints.filter(status='pending', archived_by_admin=False).count(),
        'in_progress': all_complaints.filter(status='in_progress', archived_by_admin=False).count(),
        'resolved': all_complaints.filter(status='resolved', archived_by_admin=False).count(),
    }
    return render(request, 'complaints/admin_dashboard.html', context)


@login_required
def view_complaint(request, complaint_id):
    """View single complaint details"""
    complaint = get_object_or_404(Complaint, id=complaint_id, student=request.user)
    
    context = {
        'complaint': complaint
    }
    return render(request, 'complaints/view_complaint.html', context)


@login_required
def archive_complaint(request, complaint_id):
    """Archive a complaint (admin only)"""
    if request.user.role != 'admin':
        messages.error(request, "Only admins can archive complaints.")
        return redirect('dashboard')
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.archived_by_admin = True
    complaint.save()
    
    messages.success(request, f"Complaint {complaint.complaint_id} has been archived. You can view it in the 'Archived' section.")
    return redirect('admin_dashboard')


@login_required
def delete_complaint(request, complaint_id):
    """Delete a complaint"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.user.role == 'admin':
        # Admin deletes from their view only, student keeps it
        complaint.deleted_by_admin = True
        complaint.save()
        messages.success(request, f"Complaint {complaint.complaint_id} has been permanently removed from your view. Student can still access it.")
        return redirect('admin_dashboard')
    
    elif complaint.student == request.user:
        # Student permanently deletes their own complaint
        complaint_id_display = complaint.complaint_id
        complaint.delete()
        messages.success(request, f"Complaint {complaint_id_display} has been deleted permanently.")
        return redirect('student_dashboard')
    
    else:
        messages.error(request, "You don't have permission to delete this complaint.")
        return redirect('dashboard')