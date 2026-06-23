import pandas as pd
import sqlite3
import re
from datetime import datetime

conn = sqlite3.connect("data/privacyguard.db")
df = pd.read_sql("SELECT * FROM raw_transactions", conn)

violations = []

def log_violation(row, check_name, article):
    violations.append({
        "customer_id": row["customer_id"],
        "transaction_id": row["transaction_id"],
        "violation_type": check_name,
        "article_reference": article,
        "details": f"{check_name} failed for {row['customer_id']}"
    })

# CHECK 1 — Consent
for _, row in df.iterrows():
    if not row["consent_given"]:
        log_violation(row, "Missing Consent", "GDPR Art.6 | DPDP S.6")

# CHECK 2 — Retention (>180 days = violation)
for _, row in df.iterrows():
    if row["data_retention_days"] > 180:
        log_violation(row, "Retention Exceeded", "GDPR Art.5(1)(e) | DPDP S.8")

# CHECK 3 — Vendor shared without consent
for _, row in df.iterrows():
    if row["vendor_shared"] and not row["consent_given"]:
        log_violation(row, "Vendor Share No Consent", "GDPR Art.5(1)(b) | DPDP S.6")

# CHECK 4 — Duplicate transaction_ids
dupes = df[df.duplicated("transaction_id", keep=False)]
for _, row in dupes.iterrows():
    log_violation(row, "Duplicate Transaction ID", "GDPR Art.5(1)(d)")

# CHECK 5 — Children without parental consent
for _, row in df.iterrows():
    if row["age"] < 18 and not row["parental_consent"]:
        log_violation(row, "Child No Parental Consent", "GDPR Art.8 | DPDP S.9")

# CHECK 6 — Invalid email
email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
for _, row in df.iterrows():
    if not re.match(email_regex, str(row["email"])):
        log_violation(row, "Invalid Email Format", "GDPR Art.5(1)(d)")

# Save violations
vdf = pd.DataFrame(violations)
vdf.to_csv("data/compliance_violations.csv", index=False)

# Save to DB
vdf.to_sql("compliance_violations", conn, if_exists="replace", index=False)

print(f"Total violations found: {len(vdf)}")
print(vdf["violation_type"].value_counts())
conn.close()