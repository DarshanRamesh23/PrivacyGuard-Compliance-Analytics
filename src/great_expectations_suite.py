import great_expectations as gx
import pandas as pd

df = pd.read_csv("data/shopEasy_raw_data.csv")

context = gx.get_context()

datasource = context.sources.add_pandas("shopEasy_source")
asset = datasource.add_dataframe_asset("transactions")
batch_request = asset.build_batch_request(dataframe=df)

suite = context.add_expectation_suite("privacyguard_suite")

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="privacyguard_suite"
)

# DQ Checks
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_not_be_null("consent_given")
validator.expect_column_values_to_not_be_null("transaction_id")
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_match_regex(
    "email",
    r'^[\w\.-]+@[\w\.-]+\.\w+$'
)
validator.expect_column_values_to_be_in_set(
    "purchase_category",
    ["Electronics","Clothing","Grocery","Health","Books","Travel"]
)

validator.save_expectation_suite()

# Run checkpoint
checkpoint = context.add_or_update_checkpoint(
    name="privacyguard_checkpoint",
    validator=validator
)

results = checkpoint.run()

# Save HTML report
context.build_data_docs()
print("great_expectations suite done.")
print(f"Success: {results.success}")