"""
URL validation to prevent SSRF (Server-Side Request Forgery) attacks.

This module provides URL validation to prevent access to internal/private resources.
"""
import ipaddress
import socket
from urllib.parse import urlparse
from typing import Tuple


def is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validate that a URL is safe to fetch (not pointing to internal/private resources).
    
    Args:
        url: The URL to validate
    
    Returns:
        (is_safe, error_message) tuple
    
    Note: This is a basic implementation for the scaffold. In production, consider:
    - Using a dedicated SSRF protection library
    - Implementing DNS rebinding protection
    - Adding URL reputation checks
    - Implementing rate limiting per domain
    """
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ('http', 'https'):
            return False, "Only HTTP and HTTPS URLs are allowed"
        
        # Get hostname
        hostname = parsed.hostname
        if not hostname:
            return False, "Invalid URL: no hostname found"
        
        # Block obvious private hostnames
        blocked_hostnames = [
            'localhost', '0.0.0.0', 
            'metadata.google.internal',  # GCP metadata
            '169.254.169.254',  # AWS/Azure metadata
        ]
        
        if hostname.lower() in blocked_hostnames:
            return False, "Access to localhost and private networks is not allowed"
        
        # Resolve hostname to IP and check if it's private
        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            
            # Check if IP is private, loopback, or link-local
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return False, f"Access to private IP addresses ({ip}) is not allowed"
                
            # Block cloud metadata endpoints
            if str(ip) == '169.254.169.254':
                return False, "Access to cloud metadata endpoints is not allowed"
                
        except (socket.gaierror, ValueError) as e:
            return False, f"Could not resolve hostname: {str(e)}"
        
        return True, ""
        
    except Exception as e:
        return False, f"URL validation error: {str(e)}"
