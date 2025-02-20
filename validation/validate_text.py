import os
import pandas as pd
import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest

# Path to extracted text file
data_file = os.path.abspath("data/Kushal_Resume.pdf.txt")

if not os.path.exists(data_file):
    print(f"Error: {data_file} not found! Run extract_text.py first.")
    exit(1)

# Load text data
with open(data_file, "r") as file:
    text_data = file.readlines()

# Convert to a Pandas DataFrame
df = pd.DataFrame({"text": text_data})

# ✅ Create Great Expectations Context
context = ge.get_context()

# ✅ Register a PandasDatasource (Legacy API)
context.add_datasource(
    name="pandas_datasource",
    class_name="Datasource",
    execution_engine={"class_name": "PandasExecutionEngine"},
    data_connectors={
        "runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"],
        }
    },
)

# ✅ Create a runtime batch request
batch_request = RuntimeBatchRequest(
    datasource_name="pandas_datasource",
    data_connector_name="runtime_data_connector",
    data_asset_name="text_validation",
    runtime_parameters={"batch_data": df},
    batch_identifiers={"default_identifier_name": "text_batch"},
)

# ✅ Create a validator
validator = context.get_validator(batch_request=batch_request)

# ✅ Define expectations
validator.expect_column_values_to_not_be_null("text")
validator.expect_column_value_lengths_to_be_between("text", 10, 5000)  # Text should not be too short or too long

# ✅ Run validation
results = validator.validate()

# ✅ Print validation results
print(results)
if not results["success"]:
    print("Validation failed!")
    exit(1)

print("Validation passed!")
