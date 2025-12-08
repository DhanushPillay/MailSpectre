"""
Email validation checker module for MailSpectre.
Performs multiple validation checks without using paid APIs.
"""

import re
import dns.resolver
import csv
import os
from pathlib import Path
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
    
    # Suspicious keywords commonly found in fraud emails
    FRAUD_KEYWORDS = {
        'prince', 'princess', 'barr', 'barrister', 'dr_', 'mallam', 'mrs_', 
        'mr_', 'madam', 'pastor', 'reverend', 'audit', 'lottery', 'winner',
        'claim', 'fund', 'inheritance', 'beneficiary', 'urgent', 'confidential',
        'transfer', 'million', 'attorney', 'bank', 'fbi', 'imf', 'un_', 'wto_'
    }
    
    # Major email providers that shouldn't be flagged even if used in fraud
    MAJOR_PROVIDERS = {
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com',
        'msn.com', 'aol.com', 'icloud.com', 'protonmail.com', 'mail.com',
        'yahoo.co.uk', 'yahoo.ca', 'yahoo.fr', 'hotmail.co.uk', 'googlemail.com'
    }
    
    def __init__(self):
        """Initialize the email checker."""
        self.dns_resolver = dns.resolver.Resolver()
        self.dns_resolver.timeout = 5
        self.dns_resolver.lifetime = 5
        
        # Load fraud database
        self.fraud_emails = self._load_fraud_database()
        self.fraud_domains = self._extract_domains_from_fraud()
        self.legitimate_companies = self._load_company_database()
    
    def _load_fraud_database(self) -> set:
        """
        Load known fraud emails from CSV file.
        
        Returns:
            set: Set of known fraudulent email addresses
        """
        fraud_emails = set()
        try:
            data_path = Path(__file__).parent / 'DATA' / 'fraud.csv'
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        email = row.get('email', '').strip().lower()
                        if email and '@' in email:
                            fraud_emails.add(email)
                print(f"[OK] Loaded {len(fraud_emails)} fraud emails from database")
            else:
                print(f"[WARNING] Fraud database not found at {data_path}")
        except Exception as e:
            print(f"[WARNING] Error loading fraud database: {e}")
        return fraud_emails
    
    def _extract_domains_from_fraud(self) -> set:
        """
        Extract unique domains from fraud emails for pattern matching.
        
        Returns:
            set: Set of domains associated with fraud
        """
        domains = set()
        for email in self.fraud_emails:
            try:
                domain = email.split('@')[1]
                domains.add(domain)
            except IndexError:
                continue
        return domains
    
    def _load_company_database(self) -> dict:
        """
        Load legitimate company emails from CSV file.
        
        Returns:
            dict: Dictionary mapping company names to email addresses
        """
        companies = {}
        try:
            data_path = Path(__file__).parent / 'DATA' / 'companies.csv'
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        company = row.get('Company Name', '').strip()
                        email = row.get('Email', '').strip().lower()
                        if company and email:
                            companies[email] = company
                print(f"[OK] Loaded {len(companies)} legitimate company emails")
            else:
                print(f"[WARNING] Company database not found at {data_path}")
        except Exception as e:
            print(f"[WARNING] Error loading company database: {e}")
        return companies
    
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
    
    def check_username_quality(self, email: str) -> dict:
        """
        Advanced username analysis based on fraud patterns.
        Analyzes the local part (username) for characteristics common in fake emails.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status, risk score, and details
        """
        try:
            username = email.split('@')[0].lower()
            issues = []
            risk_score = 0  # Higher score = more suspicious
            
            # Pattern 1: Very short usernames (1-3 chars) - uncommon for real users
            if len(username) <= 3:
                issues.append('Very short username')
                risk_score += 15
            
            # Pattern 2: Very long usernames (20+ chars) - often random
            elif len(username) >= 20:
                issues.append('Unusually long username')
                risk_score += 10
            
            # Pattern 3: Random character sequences (like "hkkyi")
            # Check for low vowel ratio - real names usually have vowels
            # But skip if contains dots or underscores (likely firstname.lastname format)
            has_separator = '.' in username or '_' in username
            vowels = sum(1 for c in username if c in 'aeiou')
            consonants = sum(1 for c in username if c.isalpha() and c not in 'aeiou')
            
            if consonants > 0 and not has_separator:
                vowel_ratio = vowels / (vowels + consonants)
                if vowel_ratio < 0.25:  # Less than 25% vowels
                    issues.append('Low vowel ratio (random-looking)')
                    risk_score += 20
            
            # Pattern 3b: Consecutive consonants (3+ in a row) - uncommon in real names
            # But exclude common patterns like "nst", "rst", "sch", "str"
            consonant_sequences = re.findall(r'[bcdfghjklmnpqrstvwxyz]{3,}', username)
            # Common legitimate consonant clusters in names
            common_clusters = ['nst', 'rst', 'sch', 'str', 'tch', 'chr', 'phr', 'thr']
            suspicious_sequences = [seq for seq in consonant_sequences 
                                   if not any(cluster in seq for cluster in common_clusters)]
            
            if suspicious_sequences and not has_separator:
                issues.append('Multiple consecutive consonants')
                risk_score += 15
            
            # Pattern 4: Excessive numbers at the end (3+ digits)
            if re.search(r'\d{3,}$', username):
                issues.append('Multiple numbers at end')
                risk_score += 15
            
            # Pattern 5: Multiple underscores (common in fraud emails)
            underscore_count = username.count('_')
            if underscore_count >= 2:
                issues.append(f'{underscore_count} underscores detected')
                risk_score += 10 * underscore_count
            
            # Pattern 6: Year patterns (2000-2025) often in fraud emails
            if re.search(r'(19|20)\d{2}', username):
                issues.append('Contains year pattern')
                risk_score += 8
            
            # Pattern 7: Repeated characters (aaa, 111, etc.)
            if re.search(r'(.)\1{2,}', username):
                issues.append('Repeated characters')
                risk_score += 12
            
            # Pattern 8: Common fraud keywords
            username_lower = username.lower()
            found_keywords = [kw for kw in self.FRAUD_KEYWORDS if kw in username_lower]
            if found_keywords:
                issues.append(f'Fraud keywords: {", ".join(found_keywords[:3])}')
                risk_score += 25 * len(found_keywords)
            
            # Pattern 9: Numbers only or starting with numbers
            if re.match(r'^\d+$', username):
                issues.append('Username is only numbers')
                risk_score += 30
            elif re.match(r'^\d', username):
                issues.append('Starts with numbers')
                risk_score += 10
            
            # Pattern 10: Short prefix + numbers (like "ab123", "xy99")
            if re.match(r'^[a-z]{1,3}\d+$', username):
                issues.append('Short prefix with numbers pattern')
                risk_score += 18
            
            # Pattern 11: Sequential characters (abc, 123, qwerty)
            if re.search(r'(abc|123|qwerty|asdf|zxcv)', username):
                issues.append('Sequential keyboard pattern')
                risk_score += 20
            
            # Pattern 12: Mixed case irregularities (CamelCase without reason)
            original_username = email.split('@')[0]
            uppercase_count = sum(1 for c in original_username if c.isupper())
            if uppercase_count > 0 and not original_username[0].isupper():
                issues.append('Irregular capitalization')
                risk_score += 5
            
            # Determine validity based on risk score
            # 0-10: Clean, 11-25: Minor concerns, 26-50: Suspicious, 51+: High risk
            is_valid = risk_score < 26
            
            if risk_score == 0:
                message = 'Username looks natural'
                details = 'No suspicious patterns detected in username'
            elif risk_score <= 10:
                message = 'Username has minor irregularities'
                details = f'Issues: {", ".join(issues)} (Risk: {risk_score})'
            elif risk_score <= 25:
                message = 'Username has some concerns'
                details = f'Issues: {", ".join(issues)} (Risk: {risk_score})'
            elif risk_score <= 50:
                message = 'Username appears suspicious'
                details = f'Multiple red flags: {", ".join(issues)} (Risk: {risk_score})'
            else:
                message = 'Username has high fraud indicators'
                details = f'Critical issues: {", ".join(issues)} (Risk: {risk_score})'
            
            return {
                'check': 'username_quality',
                'valid': is_valid,
                'risk_score': risk_score,
                'message': message,
                'details': details,
                'issues': issues
            }
            
        except IndexError:
            return {
                'check': 'username_quality',
                'valid': False,
                'risk_score': 100,
                'message': 'Invalid email format',
                'details': 'Cannot extract username from email',
                'issues': ['Invalid format']
            }
        except Exception as e:
            return {
                'check': 'username_quality',
                'valid': True,
                'risk_score': 0,
                'message': 'Username analysis error',
                'details': str(e),
                'issues': []
            }
    
    def check_fraud_database(self, email: str) -> dict:
        """
        Check if email exists in the fraud database.
        
        Args:
            email: Email address to check
            
        Returns:
            dict: Validation result with status and details
        """
        try:
            email_lower = email.strip().lower()
            
            # Check exact match in fraud database
            if email_lower in self.fraud_emails:
                return {
                    'check': 'fraud_database',
                    'valid': False,
                    'message': 'Email found in fraud database',
                    'details': 'This email address is flagged as fraudulent/spam'
                }
            
            # Check if it's a legitimate company email
            if email_lower in self.legitimate_companies:
                company = self.legitimate_companies[email_lower]
                return {
                    'check': 'fraud_database',
                    'valid': True,
                    'message': 'Verified company email',
                    'details': f'Official email for {company}'
                }
            
            # Check if domain is associated with fraud
            # Exclude major providers as they're used by everyone
            try:
                domain = email_lower.split('@')[1]
                if domain in self.fraud_domains and domain not in self.MAJOR_PROVIDERS:
                    return {
                        'check': 'fraud_database',
                        'valid': False,
                        'message': 'Domain associated with fraud',
                        'details': f'Domain {domain} has known fraudulent activity'
                    }
            except IndexError:
                pass
            
            # Not found in either database - neutral result
            return {
                'check': 'fraud_database',
                'valid': True,
                'message': 'Not in fraud database',
                'details': 'Email not found in known fraud or verified company lists'
            }
            
        except Exception as e:
            return {
                'check': 'fraud_database',
                'valid': True,  # Assume valid if check fails
                'message': 'Fraud check error',
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
            self.check_suspicious_patterns(email),
            self.check_username_quality(email),  # New advanced check
            self.check_fraud_database(email)
        ]
        
        # Calculate validity score
        valid_checks = sum(1 for check in checks if check['valid'])
        total_checks = len(checks)
        score = (valid_checks / total_checks) * 100
        
        # Determine overall validity
        # Email is considered valid if it passes format, domain, and MX checks
        critical_checks = ['format', 'domain_exists', 'mx_records', 'fraud_database']
        critical_passed = all(
            check['valid'] for check in checks 
            if check['check'] in critical_checks
        )
        
        # Extra penalty: if found in fraud database, automatically invalid
        fraud_check = next((c for c in checks if c['check'] == 'fraud_database'), None)
        is_fraud = fraud_check and not fraud_check['valid']
        
        return {
            'email': email,
            'valid': critical_passed and valid_checks >= 5 and not is_fraud,  # At least 5 out of 6 checks
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
