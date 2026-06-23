import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')
random.seed(42)

def random_date(start_days_ago=365, end_days_ago=0):
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    return start + (end - start) * random.random()

records = []

for i in range(1, 10001):
    age = random.randint(13, 75)
    consent = random.choices([True, False], weights=[92, 8])[0]
    consent_date = random_date(300, 10)
    transaction_date = random_date(200, 1)
    retention_days = (datetime.now() - consent_date).days
    vendor_shared = random.choices([True, False], weights=[30, 70])[0]
    parental_consent = True if age >= 18 else random.choices([True, False], weights=[60, 40])[0]

    # inject duplicate transaction_ids for ~2% rows
    txn_id = f"TXN{random.randint(1, 9800):05d}"

    records.append({
        "customer_id": f"CUST{i:05d}",
        "name": fake.name(),
        "email": fake.email() if random.random() > 0.03 else "invalid-email",
        "phone": fake.phone_number(),
        "age": age,
        "parental_consent": parental_consent,
        "consent_given": consent,
        "consent_date": consent_date.strftime("%Y-%m-%d"),
        "transaction_id": txn_id,
        "amount": round(random.uniform(100, 50000), 2),
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "data_retention_days": retention_days,
        "purchase_category": random.choice([
            "Electronics", "Clothing", "Grocery",
            "Health", "Books", "Travel"
        ]),
        "vendor_shared": vendor_shared,
        "location": fake.city()
    })

df = pd.DataFrame(records)
df.to_csv("data/shopEasy_raw_data.csv", index=False)
print(f"Dataset generated: {len(df)} records")
print(df.head())