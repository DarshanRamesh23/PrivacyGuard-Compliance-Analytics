# PrivacyGuard — Privacy Compliance Audit Dashboard

## Business Problem
Organizations processing personal data face significant 
regulatory exposure under GDPR and India's DPDP Act 2023. 
Manual compliance reviews are slow, inconsistent, and 
lack audit trails. ShopEasy India (fictional e-commerce 
company) needed an automated system to continuously 
monitor data processing activities and flag violations 
before regulators do.

## Solution Overview
PrivacyGuard is an automated privacy compliance audit 
pipeline that ingests customer transaction data, runs 
6 regulatory compliance checks tagged to specific GDPR 
articles and DPDP Act sections, logs a full audit trail, 
and delivers findings via a 3-page Power BI dashboard 
that a Data Protection Officer can act on directly.

## Compliance Framework
| Regulation | Coverage |
|---|---|
| GDPR | Art.5 (principles), Art.6 (consent), Art.8 (children), Art.28 (processors), Art.32 (security), Art.35 (DPIA) |
| India DPDP Act 2023 | S.6 (consent), S.8 (retention), S.9 (children) |

## Architecture
Raw Data (CSV)

↓

generate_data.py — Synthetic data generation (Faker)

↓

load_to_sqlite.py — SQLite ingestion

↓

compliance_checks.py — 6 privacy compliance checks

↓

audit_logger.py — Audit trail logging

↓

great_expectations_suite.py — DQ validation layer

↓

Power BI Dashboard — 3-page executive reporting

## Compliance Checks Implemented
| Check | Rule | GDPR Article | DPDP Section |
|---|---|---|---|
| Consent Check | consent_given must be True | Art.6 | S.6 |
| Retention Check | data_retention_days ≤ 180 | Art.5(1)(e) | S.8 |
| Vendor Share Check | vendor_shared=True only if consent=True | Art.5(1)(b) | S.6 |
| Duplicate Check | No duplicate transaction_ids | Art.5(1)(d) | — |
| Children's Data | age<18 requires parental_consent=True | Art.8 | S.9 |
| Email Validity | Valid email format required | Art.5(1)(d) | — |

## Key Findings (Sample Run — 10,000 Records)
| Violation | Count | Rate |
|---|---|---|
| Duplicate Transaction ID | 6,348 | 63.48% |
| Retention Exceeded | 3,991 | 39.91% |
| Missing Consent | 734 | 7.34% |
| Child No Parental Consent | 307 | 3.07% |
| Invalid Email Format | 285 | 2.85% |
| Vendor Share No Consent | 214 | 2.14% |

## Dashboard
3-page Power BI dashboard:
- Page 1: Executive Summary — KPI cards, violation distribution
- Page 2: Violation Detail — drilldown table with GDPR/DPDP article tags + slicers
- Page 3: Audit Log — full check history with violation rates

## Documents
- DPIA_ShopEasy_VendorSharing.pdf — Mock Data Protection Impact Assessment
- Compliance_Findings_Memo.pdf — Consultant-style findings memo to DPO

## Tech Stack
Python | Pandas | Faker | SQLite | great_expectations | Power BI

## How to Run
```bash
pip install faker pandas great_expectations
python src/generate_data.py
python src/load_to_sqlite.py
python src/compliance_checks.py
python src/audit_logger.py
python src/great_expectations_suite.py
# Open dashboard/PrivacyGuard_Dashboard.pbix in Power BI Desktop
```

## Author
Darshan Ramesh T | github.com/DarshanRamesh23