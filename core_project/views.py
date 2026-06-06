from django.shortcuts import render, redirect
from django.contrib import messages
from school.models import Client, Domain

def school_search_view(request):
    """
    Handles the public-facing landing page search.
    Queries the public database schema for a matching school client name
    and redirects the browser to that tenant's configured primary domain.
    """
    if request.method == 'POST':
        # Retrieve and clean up the school name from the form input
        school_name = request.POST.get('school_name', '').strip()
        
        if not school_name:
            messages.error(request, "Please enter a school name to search.")
            return render(request, 'home.html')

        # 1. Look for the tenant client matching the name (case-insensitive lookup)
        tenant = Client.objects.filter(name__icontains=school_name).first()
        
        if tenant:
            # 2. Get the primary domain record assigned to this tenant
            domain = Domain.objects.filter(tenant=tenant, is_primary=True).first()
            
            if domain:
                # 3. Construct the URL dynamically to handle local ports (e.g., :8000)
                # request.get_port() fetches '8000' during local dev or remains blank in prod.
                current_port = request.get_port()
                port_suffix = f":{current_port}" if current_port and current_port not in ('80', '443') else ""
                
                # Build the complete redirect string
                target_url = f"http://{domain.domain}{port_suffix}"
                return redirect(target_url)
            else:
                messages.error(request, f"'{tenant.name}' was found, but it has no primary domain configured.")
        else:
            messages.error(request, "School not found. Please verify the name and try again.")
            
    # Default GET request rendering the home landing page
    return render(request, 'home.html')
