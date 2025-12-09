# Username Quality Detection Algorithm

## Overview
This document describes the advanced pattern-based algorithm used to detect fake emails by analyzing username characteristics.

## Algorithm Details

### Risk Scoring System
The algorithm assigns risk points (0-100+) based on suspicious patterns:
- **0-10**: Clean - No concerns
- **11-25**: Minor concerns - Some irregularities
- **26-50**: Suspicious - Multiple red flags
- **51+**: High risk - Critical fraud indicators

Emails with a risk score of 26 or higher are flagged as suspicious.

### Detection Patterns

#### 1. **Very Short Usernames (15 points)**
- Usernames with 1-3 characters (e.g., `ab@`, `xyz@`)
- Uncommon for real users

#### 2. **Very Long Usernames (10 points)**
- Usernames with 20+ characters
- Often indicates random generation

#### 3. **Low Vowel Ratio (20 points)**
- Less than 25% vowels in username
- Example: `hkkyi` has only 20% vowels (1 out of 5 letters)
- Real names typically have more vowels
- **Exception**: Skipped for emails with dots or underscores (firstname.lastname format)

#### 4. **Consecutive Consonants (15 points)**
- 3+ consecutive consonants (e.g., `hkkyi`, `xyzqrs`)
- Excludes common legitimate patterns: `nst`, `rst`, `sch`, `str`, `tch`, `chr`
- **Exception**: Skipped for emails with separators (dot/underscore)

#### 5. **Multiple Numbers at End (15 points)**
- 3+ digits at the end (e.g., `user2003`, `name123`)
- Common in automated/fake accounts

#### 6. **Multiple Underscores (10 points per underscore)**
- 2+ underscores indicate automated generation
- Example: `user_name_123_abc` = 30 points

#### 7. **Year Patterns (8 points)**
- Contains years like 2000-2025 or 1900-1999
- Example: `user2003`, `name1990`

#### 8. **Repeated Characters (12 points)**
- Same character 3+ times (e.g., `aaa`, `111`)

#### 9. **Fraud Keywords (25 points per keyword)**
- Keywords like: `prince`, `barr`, `dr_`, `mallam`, `pastor`, `lottery`
- Example: `prince_charles` triggers this

#### 10. **Numbers Only (30 points)**
- Username is entirely numbers
- Or starts with numbers (10 points)

#### 11. **Short Prefix + Numbers (18 points)**
- Pattern like `ab123`, `xy99` (1-3 letters + numbers)

#### 12. **Sequential Patterns (20 points)**
- Keyboard sequences: `abc`, `123`, `qwerty`, `asdf`

#### 13. **Irregular Capitalization (5 points)**
- CamelCase without proper formatting

## Examples

### Suspicious Emails Detected

```
hkkyi@gmail.com
├─ Low vowel ratio: 20 points
├─ Consecutive consonants (hkk): 15 points
└─ Total Risk: 35 → SUSPICIOUS

prince_charles2003@yahoo.com
├─ Multiple numbers at end (2003): 15 points
├─ Year pattern: 8 points
├─ Fraud keyword (prince): 25 points
└─ Total Risk: 48 → SUSPICIOUS

test123@example.com
├─ Multiple numbers at end: 15 points
├─ Sequential pattern (test): 20 points
└─ Total Risk: 35 → SUSPICIOUS
```

### Clean Emails

```
john.smith@gmail.com
└─ Total Risk: 0 → CLEAN (separator exceptions apply)

sarah.johnson@company.com
└─ Total Risk: 0 → CLEAN (separator exceptions apply)

jdoe@company.com
└─ Total Risk: 0 → CLEAN
```

## Integration

The username quality check is integrated into the main validation pipeline along with:
1. Format validation
2. Domain DNS verification
3. MX record checking
4. Disposable email detection
5. **Username quality analysis** (NEW)
6. Fraud database matching

## Database Reference

The algorithm is informed by analyzing 1,305 fraudulent emails in our database, which revealed:
- 37.2% contain numbers
- 23.8% have multiple numbers at the end
- 21.0% use underscores
- 5.7% contain year patterns
- Common fraud prefixes: prince, barr, mallam, dr_, mrs_, pastor

## Usage

The algorithm automatically runs when validating any email:

```python
from checker import EmailChecker

checker = EmailChecker()
result = checker.validate_email('hkkyi@gmail.com')

print(f"Valid: {result['valid']}")
print(f"Score: {result['score']}%")
# Check username_quality in result['checks'] for details
```

## Future Improvements

1. Machine learning model trained on fraud patterns
2. Domain reputation scoring
3. Real-time API integration for enhanced detection
4. Geographic pattern analysis
5. Typosquatting detection for company domains
