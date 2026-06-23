import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("data/privacyguard.db")

df = pd.read_sql("SELECT * FROM raw_transactions", conn)
vdf = pd.read_sql("SELECT * FROM compliance_violations", conn)

total = len(df)
checks = [
    ("Missing Consent",          "GDPR Art.6 | DPDP S.6"),
    ("Retention Exceeded",       "GDPR Art.5(1)(e) | DPDP S.8"),
    ("Vendor Share No Consent",  "GDPR Art.5(1)(b) | DPDP S.6"),
    ("Duplicate Transaction ID", "GDPR Art.5(1)(d)"),
    ("Child No Parental Consent","GDPR Art.8 | DPDP S.9"),
    ("Invalid Email Format",     "GDPR Art.5(1)(d)"),
]

logs = []
for check_name, article in checks:
    count = len(vdf[vdf["violation_type"] == check_name])
    logs.append({
        "check_name": check_name,
        "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records_checked": total,
        "violations_found": count,
        "violation_rate_percent": round((count / total) * 100, 2),
        "article_reference": article
    })

log_df = pd.DataFrame(logs)
log_df.to_sql("audit_log", conn, if_exists="replace", index=False)

print("Audit log written.")
print(log_df[["check_name","violations_found","violation_rate_percent"]])
conn.close()