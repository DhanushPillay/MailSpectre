"""
Email validation checker module for MailSpectre.
Performs multiple validation checks without using paid APIs.
"""

import re
import dns.resolver
from urllib.parse import urlparse


class EmailChecker:
    """
    Comprehensive email validation checker.
    Performs format, DNS, MX, disposable, and pattern checks.
    """
    
    # List of known disposable email domains
    DISPOSABLE_DOMAINS = {
        'tempmail.com', 'guerrillamail.com', '10minutemail.com', 'mailinator.com',
        'throwaway.email', 'temp-mail.org', 'fakeinbox.com', 'maildrop.cc',
        'getnada.com', 'trashmail.com', 'yopmail.com', 'sharklasers.com',
        'guerrillamailblock.com', 'grr.la', 'mintemail.com', 'tempmail.net',
        'dispostable.com', 'mailnesia.com', 'spambox.us', 'mohmal.com'
    }
    
    # Suspicious patterns that might indicate fake emails
    SUSPICIOUS_PATTERNS = [
        r'test\d+@',
        r'fake\d*@',
        r'spam\d*@',
        r'trash\d*@',
        r'temp\d*@',
        r'dummy\d*@',
        r'asdf',
        r'qwerty',
        r'12345',
        r'[a-z]{20,}',  # Very long random character sequences
        r'^\d+@',  # Starting with only numbers
    ]
    
    def __init__(self):
        """Initialize the email checker."""
        self.dns_resolver = dns.resolver.Resolver()
        self.dns_resolver.timeout = 5
        self.dns_resolver.lifetime = 5
    
    def validate_format(self, email: str) -> dict:
        """
        Validate email format using regex.
        
        Args:
            email: Email address to validate
            
        Returns:
            dict: Validation result with status and details
        """
        # RFC 5322 compliant regex (simplified but comprehensive)
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        try:
            is_valid = bool(re.match(email_regex, email))
            return {
                'check': 'format',
                'valid': is_valid,
                'message': 'Valid email format' if is_valid else 'Invalid email format',
                'details': 'Email follows standard format' if is_valid else 'Email does not match RFC 5322 format'
            }
        except Exception as e:
            return {
                'check': 'format',
                'valid': False,
                'message': 'Format validation error',
                'details': str(e)
            }
    
    def check_domain_exists(self, email: str) -> dict:
        """
        Check if the domain exists using DNS lookup.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status and details
        """
        try:
            domain = email.split('@')[1]
            
            # Try to resolve domain to check if it exists
            try:
                answers = self.dns_resolver.resolve(domain, 'A')
                return {
                    'check': 'domain_exists',
                    'valid': True,
                    'message': 'Domain exists',
                    'details': f'Domain {domain} has valid DNS records'
                }
            except dns.resolver.NXDOMAIN:
                return {
                    'check': 'domain_exists',
                    'valid': False,
                    'message': 'Domain does not exist',
                    'details': f'Domain {domain} not found in DNS'
                }
            except dns.resolver.NoAnswer:
                return {
                    'check': 'domain_exists',
                    'valid': False,
                    'message': 'Domain has no records',
                    'details': f'Domain {domain} exists but has no A records'
                }
            except dns.resolver.Timeout:
                return {
                    'check': 'domain_exists',
                    'valid': False,
                    'message': 'DNS lookup timeout',
                    'details': 'Could not verify domain due to timeout'
                }
                
        except IndexError:
            return {
                'check': 'domain_exists',
                'valid': False,
                'message': 'Invalid email format',
                'details': 'Cannot extract domain from email'
            }
        except Exception as e:
            return {
                'check': 'domain_exists',
                'valid': False,
                'message': 'Domain check error',
                'details': str(e)
            }
    
    def check_mx_records(self, email: str) -> dict:
        """
        Check if domain has MX (Mail Exchange) records.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status and details
        """
        try:
            domain = email.split('@')[1]
            
            try:
                mx_records = self.dns_resolver.resolve(domain, 'MX')
                mx_list = [str(mx.exchange) for mx in mx_records]
                
                return {
                    'check': 'mx_records',
                    'valid': True,
                    'message': 'MX records found',
                    'details': f'Domain has {len(mx_list)} mail server(s): {", ".join(mx_list[:3])}'
                }
            except dns.resolver.NXDOMAIN:
                return {
                    'check': 'mx_records',
                    'valid': False,
                    'message': 'No MX records',
                    'details': f'Domain {domain} has no mail servers configured'
                }
            except dns.resolver.NoAnswer:
                return {
                    'check': 'mx_records',
                    'valid': False,
                    'message': 'No MX records',
                    'details': f'Domain {domain} exists but has no MX records'
                }
            except dns.resolver.Timeout:
                return {
                    'check': 'mx_records',
                    'valid': False,
                    'message': 'MX lookup timeout',
                    'details': 'Could not verify MX records due to timeout'
                }
                
        except IndexError:
            return {
                'check': 'mx_records',
                'valid': False,
                'message': 'Invalid email format',
                'details': 'Cannot extract domain from email'
            }
        except Exception as e:
            return {
                'check': 'mx_records',
                'valid': False,
                'message': 'MX check error',
                'details': str(e)
            }
    
    def check_disposable(self, email: str) -> dict:
        """
        Check if email is from a disposable email provider.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status and details
        """
        try:
            domain = email.split('@')[1].lower()
            
            is_disposable = domain in self.DISPOSABLE_DOMAINS
            
            return {
                'check': 'disposable',
                'valid': not is_disposable,
                'message': 'Disposable email detected' if is_disposable else 'Not a disposable email',
                'details': f'Domain {domain} is in disposable list' if is_disposable else 'Domain not in known disposable providers'
            }
            
        except IndexError:
            return {
                'check': 'disposable',
                'valid': False,
                'message': 'Invalid email format',
                'details': 'Cannot extract domain from email'
            }
        except Exception as e:
            return {
                'check': 'disposable',
                'valid': True,  # Assume not disposable if check fails
                'message': 'Disposable check error',
                'details': str(e)
            }
    
    def check_suspicious_patterns(self, email: str) -> dict:
        """
        Check for suspicious patterns in the email address.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status and details
        """
        try:
            suspicious_found = []
            
            for pattern in self.SUSPICIOUS_PATTERNS:
                if re.search(pattern, email.lower()):
                    suspicious_found.append(pattern)
            
            is_valid = len(suspicious_found) == 0
            
            return {
                'check': 'suspicious_patterns',
                'valid': is_valid,
                'message': 'Suspicious patterns detected' if not is_valid else 'No suspicious patterns',
                'details': f'Found {len(suspicious_found)} suspicious pattern(s)' if not is_valid else 'Email looks legitimate'
            }
            
        except Exception as e:
            return {
                'check': 'suspicious_patterns',
                'valid': True,  # Assume valid if check fails
                'message': 'Pattern check error',
                'details': str(e)
            }
    
    def validate_email(self, email: str) -> dict:
        """
        Perform all validation checks on an email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            dict: Complete validation results
        """
        if not email or not isinstance(email, str):
            return {
                'email': email,
                'valid': False,
                'score': 0,
                'checks': [],
                'summary': 'Invalid input: Email must be a non-empty string'
            }
        
        email = email.strip().lower()
        
        # Perform all checks
        checks = [
            self.validate_format(email),
            self.check_domain_exists(email),
            self.check_mx_records(email),
            self.check_disposable(email),
            self.check_suspicious_patterns(email)
        ]
        
        # Calculate validity score
        valid_checks = sum(1 for check in checks if check['valid'])
        total_checks = len(checks)
        score = (valid_checks / total_checks) * 100
        
        # Determine overall validity
        # Email is considered valid if it passes format, domain, and MX checks
        critical_checks = ['format', 'domain_exists', 'mx_records']
        critical_passed = all(
            check['valid'] for check in checks 
            if check['check'] in critical_checks
        )
        
        return {
            'email': email,
            'valid': critical_passed and valid_checks >= 4,  # At least 4 out of 5 checks
            'score': round(score, 2),
            'checks': checks,
            'summary': self._generate_summary(checks, score)
        }
    
    def _generate_summary(self, checks: list, score: float) -> str:
        """
        Generate a human-readable summary of validation results.
        
        Args:
            checks: List of check results
            score: Validation score
            
        Returns:
            str: Summary message
        """
        failed_checks = [check['check'] for check in checks if not check['valid']]
        
        if score == 100:
            return 'Email passed all validation checks'
        elif score >= 80:
            return f'Email looks valid with minor concerns: {", ".join(failed_checks)}'
        elif score >= 60:
            return f'Email has some issues: {", ".join(failed_checks)}'
        else:
            return f'Email appears invalid or suspicious: {", ".join(failed_checks)}'
