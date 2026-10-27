# ============================================================

# E-COMMERCE SALES & CUSTOMER INSIGHTS
# Dataset: UCI Online Retail
# Tools: Python, Pandas, NumPy
#
# Important:
# 1. original_df is never modified.
# 2. cleaned_df contains safely prepared data.
# 3. analysis_df has exact duplicate rows removed.
# 4. Unusual transactions are investigated, not automatically deleted.

# ============================================================

import numpy as np
import pandas as pd
from pathlib import Path # Path helps us work with file and folder paths.

# ============================================================

# SECTION 1: LOAD DATASET

# ============================================================

file_path = Path(r"C:\Users\alok3\OneDrive\Desktop\Programming  Language" r"\Main_project\Online_Retail.xlsx")
# r stands for raw string, not read.
# Code                  Meaning of r
# r"C:\folder"           Raw string
# open("data.txt", "r")  Read mode
# A raw string tells Python to treat backslashes () as literal characters rather than interpreting them as escape sequences. We can also write the entire path as a single raw string.

if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")
# raise is a Python keyword used to intentionally generate an exception (error) when a particular condition occurs.

df = pd.read_excel(file_path)
original_df = df.copy(deep=True)
cleaned_df = df.copy(deep=True)
# creates a separate copy of the DataFrame.
# deep=True means Pandas creates a deep copy of the DataFrame's data and structure, rather than just creating a new reference to the same DataFrame.

original_columns = list(original_df.columns)
# original_df.columns provides the column names, and list() converts them into a Python list stored in original_columns.

original_rows = len(original_df)
# total number of rows in the data frame.

required_columns = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
missing_columns = [column for column in required_columns if column not in original_df.columns]
# missing_columns will contain [] empty list, because all required columns exists in original_df, and if not present then add only columns names.

if missing_columns:
    raise ValueError(f"Required columns are missing: {missing_columns}")
print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)
print("Dataset shape:", original_df.shape)
print("Total rows:", len(original_df))
print("Total columns:", len(original_df.columns))
print("\nColumn names:")
print(original_df.columns.tolist())
# .tolist() converts the column names into a regular Python list.

# ============================================================

# SECTION 2: MISSING VALUES

# ============================================================

print("\n" + "=" * 70)
print("2. MISSING VALUES")
print("=" * 70)
missing_report = pd.DataFrame({"Missing_Count": original_df.isna().sum(),"Missing_Percentage": (original_df.isna().sum() / len(original_df) * 100).round(2)})
# original_df.isna() identifies missing values and returns a Boolean DataFrame: True- where a value is missing and False- where it is present. .sum() counts the True values in each column. Since isna() marks missing values as True, the result gives the number of missing values in each column.

print(missing_report.to_string())
# Without .to_string(): Pandas may show only some rows and display ... when the output is too large.
# With .to_string(): It displays all rows of the DataFrame as text.

print("\nMissing values in Description:",int(original_df["Description"].isna().sum()))
# int() converts the missing-value count into an integer.

print("Missing values in CustomerID:",int(original_df["CustomerID"].isna().sum()))

# ============================================================

# SECTION 3: INVESTIGATE MISSING DESCRIPTIONS

# ============================================================

print("\n" + "=" * 70)
print("3. MISSING DESCRIPTION INVESTIGATION")
print("=" * 70)
missing_description = original_df[original_df["Description"].isna()]
# selects and stores every complete row where Description is missing.

print("Missing descriptions:", (missing_description))
print("Missing descriptions with zero price:", int(missing_description["UnitPrice"].eq(0).sum()))
# counts how many rows have a UnitPrice equal to zero. .eq(0) returns True for zero prices and False for other values. .sum() counts the True values.
# int() converts the result of the expression inside it into an integer.

print("Missing descriptions with non-zero price:",int(missing_description["UnitPrice"].ne(0).sum()))
# .ne(0) means not equal to zero. It returns True for prices that are not zero and False for prices that are zero. .sum() counts the True values.

print("\nSample rows:")
print(missing_description.head(10).to_string(index=False))
# to_string(index=False) → Displays the DataFrame as text, without row numbers.
# to_string() → Displays the DataFrame as text, including row numbers.

# ============================================================

# SECTION 4: EXACT DUPLICATE AUDIT

# ============================================================

print("\n" + "=" * 70)
print("4. EXACT DUPLICATE AUDIT")
print("=" * 70)
exact_duplicate_rows = int(original_df.duplicated().sum())
# df.duplicated() → Har row check karta hai ki woh pehle kisi row mein aa chuki hai ya nahi. Default mein first occurrence ko False aur uske baad wali identical rows ko True mark karta hai.

print("Original rows:", len(original_df))
print("Extra exact duplicate rows:", exact_duplicate_rows)
print("Rows belonging to duplicate groups:", int(original_df.duplicated(keep=False).sum()))
# df.duplicated(keep=False).sum() → Duplicate groups ki saari rows, including first occurrence, count karta hai.

invoice_counts = original_df["InvoiceNo"].value_counts(dropna=False)
# Har invoice number kitni baar aaya hai, uska count milta hai. dropna=False ka matlab missing invoice values ko bhi count mein include karna.

print("Unique invoice numbers:",original_df["InvoiceNo"].nunique(dropna=True))
# .nunique() counts the number of different (unique) invoice numbers. dropna=True means missing values (NaN) ko count nahi karega.

print("Invoice numbers appearing more than once:",int((invoice_counts > 1).sum()))
print("\nSample exact duplicate rows:")
print(original_df[original_df.duplicated(keep=False)].head(10).to_string(index=False))

# ============================================================

# SECTION 5: DATA TYPES AND TEXT QUALITY

# ============================================================

print("\n" + "=" * 70)
print("5. DATA TYPES AND TEXT QUALITY")
print("=" * 70)
print("\nOriginal data types:")
print(original_df.dtypes)
text_columns = [
    "InvoiceNo", "StockCode", "Description", "Country"
]
for column in text_columns:
    values = original_df[column].dropna().astype(str)
    outer_spaces = int(
        values.ne(values.str.strip()).sum()
    )
    blank_values = int(
        values.str.strip().eq("").sum()
    )
    print(f"\n{column}")
    print("Values with outer spaces:", outer_spaces)
    print("Blank or whitespace-only values:", blank_values)
print("\nUnique countries:", original_df["Country"].nunique())
print("Unique stock codes:", original_df["StockCode"].nunique())

# ============================================================

# SECTION 6: QUANTITY AND UNIT PRICE AUDIT

# ============================================================

print("\n" + "=" * 70)
print("6. QUANTITY AND UNIT PRICE AUDIT")
print("=" * 70)
quantity_report = pd.Series({
    "Positive": int((original_df["Quantity"] > 0).sum()),
    "Zero": int((original_df["Quantity"] == 0).sum()),
    "Negative": int((original_df["Quantity"] < 0).sum()),
    "Missing": int(original_df["Quantity"].isna().sum())
})
price_report = pd.Series({
    "Positive": int((original_df["UnitPrice"] > 0).sum()),
    "Zero": int((original_df["UnitPrice"] == 0).sum()),
    "Negative": int((original_df["UnitPrice"] < 0).sum()),
    "Missing": int(original_df["UnitPrice"].isna().sum())
})
print("\nQuantity categories:")
print(quantity_report.to_string())
print("\nUnitPrice categories:")
print(price_report.to_string())
print("\nNegative quantity examples:")
print(
    original_df.loc[
        original_df["Quantity"] < 0,
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice", "CustomerID"
        ]
    ].head(10).to_string(index=False)
)
print("\nZero-price examples:")
print(
    original_df.loc[
        original_df["UnitPrice"] == 0,
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice", "CustomerID"
        ]
    ].head(10).to_string(index=False)
)
print("\nNegative-price examples:")
print(
    original_df.loc[
        original_df["UnitPrice"] < 0,
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice", "CustomerID"
        ]
    ].head(10).to_string(index=False)
)

# ============================================================

# SECTION 7: CANCELLATIONS AND RETURNS

# ============================================================

print("\n" + "=" * 70)
print("7. CANCELLATION AND RETURN AUDIT")
print("=" * 70)
original_invoice_text = (
    original_df["InvoiceNo"].astype("string").str.strip()
)
original_cancellation_mask = (
    original_invoice_text.str.startswith("C", na=False)
)
print(
    "Rows with C-prefixed invoice numbers:",
    int(original_cancellation_mask.sum())
)
print(
    "Unique C-prefixed invoice numbers:",
    int(original_invoice_text[original_cancellation_mask].nunique())
)
print(
    "Rows with negative quantities:",
    int((original_df["Quantity"] < 0).sum())
)
print("\nSample C-prefixed invoices:")
print(
    original_df.loc[
        original_cancellation_mask,
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice", "InvoiceDate"
        ]
    ].head(10).to_string(index=False)
)
print(
    "\nNote: cancellation prefixes and negative quantities are "
    "indicators, not interchangeable definitions."
)

# ============================================================

# SECTION 8: CUSTOMER ID VALIDATION

# ============================================================

print("\n" + "=" * 70)
print("8. CUSTOMER ID VALIDATION")
print("=" * 70)
numeric_customer_ids = pd.to_numeric(
    original_df["CustomerID"], errors="coerce"
)
invalid_customer_id_mask = (
    numeric_customer_ids.notna()
    & (
        (numeric_customer_ids % 1 != 0)
        | (numeric_customer_ids <= 0)
    )
)
print(
    "Missing CustomerIDs:",
    int(original_df["CustomerID"].isna().sum())
)
print(
    "CustomerIDs that are not positive whole numbers:",
    int(invalid_customer_id_mask.sum())
)
print("\nMissing CustomerID sample:")
print(
    original_df.loc[
        original_df["CustomerID"].isna()
    ].head(10).to_string(index=False)
)

# ============================================================

# SECTION 9: DATE AUDIT

# ============================================================

print("\n" + "=" * 70)
print("9. DATE AUDIT")
print("=" * 70)
parsed_original_dates = pd.to_datetime(
    original_df["InvoiceDate"], errors="coerce"
)
print(
    "Originally missing dates:",
    int(original_df["InvoiceDate"].isna().sum())
)
print(
    "Dates that fail parsing:",
    int(parsed_original_dates.isna().sum())
)
valid_original_dates = parsed_original_dates.dropna()
if not valid_original_dates.empty:
    print("Earliest date:", valid_original_dates.min())
    print("Latest date:", valid_original_dates.max())
    print(
        "Dates later than current date:",
        int(
            (
                valid_original_dates
                > pd.Timestamp.now().normalize()
            ).sum()
        )
    )

# ============================================================

# SECTION 10: EXTREME VALUE INVESTIGATION

# ============================================================

print("\n" + "=" * 70)
print("10. EXTREME VALUE INVESTIGATION")
print("=" * 70)
print("\nQuantity summary:")
print(
    original_df["Quantity"].describe(
        percentiles=[0.01, 0.25, 0.50, 0.75, 0.99]
    )
)
print("\nUnitPrice summary:")
print(
    original_df["UnitPrice"].describe(
        percentiles=[0.01, 0.25, 0.50, 0.75, 0.99]
    )
)
print("\nLargest positive quantities:")
print(
    original_df.nlargest(10, "Quantity")[
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice"
        ]
    ].to_string(index=False)
)
print("\nLargest unit prices:")
print(
    original_df.nlargest(10, "UnitPrice")[
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "UnitPrice"
        ]
    ].to_string(index=False)
)

# ============================================================

# SECTION 11: SAFE DATA PREPARATION

# ============================================================

print("\n" + "=" * 70)
print("11. SAFE DATA PREPARATION")
print("=" * 70)
# Trim outer spaces without filling missing values.
# This modifies cleaned_df only, not original_df.

for column in text_columns:
    cleaned_df[column] = cleaned_df[column].map(
        lambda value: (
            value.strip() if isinstance(value, str) else value
        )
    )
# Keep identifiers as text.

cleaned_df["InvoiceNo"] = cleaned_df["InvoiceNo"].astype("string")
cleaned_df["StockCode"] = cleaned_df["StockCode"].astype("string")
# Parse dates in the working copy.

cleaned_df["InvoiceDate"] = pd.to_datetime(
    cleaned_df["InvoiceDate"], errors="coerce"
)
print("Rows before preparation:", original_rows)
print("Rows after preparation:", len(cleaned_df))
print("Rows removed during preparation:", original_rows - len(cleaned_df))
print("\nPrepared data types:")
print(cleaned_df.dtypes)
assert len(cleaned_df) == len(original_df), (
    "Safe preparation unexpectedly changed the row count."
)
assert original_df.equals(df), (
    "The original dataset has been modified."
)

# ============================================================

# SECTION 12: ANALYSE DUPLICATES AFTER TEXT TRIMMING

# ============================================================

print("\n" + "=" * 70)
print("12. DUPLICATE AUDIT AFTER TEXT TRIMMING")
print("=" * 70)
duplicates_before_trimming = int(original_df.duplicated().sum())
duplicates_after_trimming = int(
    cleaned_df.duplicated(subset=original_columns).sum()
)
print(
    "Exact duplicate rows before trimming:",
    duplicates_before_trimming
)
print(
    "Exact duplicate rows after trimming:",
    duplicates_after_trimming
)
print(
    "Change in duplicate count:",
    duplicates_after_trimming - duplicates_before_trimming
)
print(
    "Note: trimming may make previously different text values identical."
)

# ============================================================

# SECTION 13: CREATE ANALYSIS FLAGS

# ============================================================

print("\n" + "=" * 70)
print("13. CREATE ANALYSIS FLAGS")
print("=" * 70)
cleaned_df["is_cancellation_invoice"] = (
    cleaned_df["InvoiceNo"].str.startswith("C", na=False)
)
cleaned_df["is_negative_quantity"] = (
    cleaned_df["Quantity"] < 0
)
cleaned_df["is_zero_price"] = (
    cleaned_df["UnitPrice"] == 0
)
cleaned_df["has_missing_description"] = (
    cleaned_df["Description"].isna()
)
cleaned_df["has_missing_customer_id"] = (
    cleaned_df["CustomerID"].isna()
)
cleaned_df["line_value"] = (
    cleaned_df["Quantity"] * cleaned_df["UnitPrice"]
)
print("Analysis flags created.")
print(
    cleaned_df[
        [
            "is_cancellation_invoice",
            "is_negative_quantity",
            "is_zero_price",
            "has_missing_description",
            "has_missing_customer_id"
        ]
    ].sum().to_string()
)

# ============================================================

# SECTION 14: INVESTIGATE A SPECIFIC INVOICE

# ============================================================

print("\n" + "=" * 70)
print("14. INVOICE 555524 INVESTIGATION")
print("=" * 70)
target_invoice = "555524"
target_invoice_mask = (
    original_df["InvoiceNo"].astype("string").str.strip()
    == target_invoice
)
if target_invoice_mask.any():
    target_positions = np.flatnonzero(
        target_invoice_mask.to_numpy()
    )
    first_position = int(target_positions[0])
    last_position = int(target_positions[-1])
    print("Invoice found:", target_invoice)
    print("Number of matching rows:", len(target_positions))
    print("First matching row position:", first_position)
    start_position = max(0, first_position - 5)
    end_position = min(len(original_df), last_position + 6)
    surrounding_rows = original_df.iloc[
        start_position:end_position
    ].copy()
    surrounding_rows.insert(
        0,
        "original_row_position",
        surrounding_rows.index
    )
    print("\nRows surrounding the actual invoice position:")
    print(surrounding_rows.to_string(index=False))
    print("\nComplete invoice contents:")
    invoice_context = original_df.loc[
        target_invoice_mask
    ].sort_values(
        "StockCode",
        key=lambda column: column.astype("string")
    )
    print(invoice_context.to_string(index=False))
else:
    print(
        f"Invoice {target_invoice} was not found. "
        "No unrelated row positions will be labelled as this invoice."
    )

# ============================================================

# SECTION 15: INVESTIGATE SELECTED PRODUCTS

# ============================================================

print("\n" + "=" * 70)
print("15. REPEATED PRODUCT INVESTIGATION")
print("=" * 70)
products_to_check = ["22698", "22697"]
product_records = cleaned_df[
    cleaned_df["StockCode"].isin(products_to_check)
].copy()
product_repeat_summary = (
    product_records.groupby(
        [
            "InvoiceNo", "StockCode", "Description",
            "Quantity", "InvoiceDate", "UnitPrice", "CustomerID"
        ],
        dropna=False,
        sort=False
    )
    .size()
    .reset_index(name="copies")
    .sort_values("copies", ascending=False)
)
print("Selected products:", products_to_check)
print("\nRepeated product records:")
print(product_repeat_summary.head(20).to_string(index=False))
print("\nMatching product rows:", len(product_records))
print(
    "Unique invoices containing selected products:",
    product_records["InvoiceNo"].nunique()
)

# ============================================================

# SECTION 16: DUPLICATE GROUP SUMMARY

# ============================================================

print("\n" + "=" * 70)
print("16. DUPLICATE GROUP SUMMARY")
print("=" * 70)
# Build duplicate groups from the prepared dataset.
# A group is an identical record; copies counts its occurrences.

all_record_groups = (
    cleaned_df.groupby(
        original_columns,
        dropna=False,
        sort=False
    )
    .size()
    .reset_index(name="copies")
)
duplicate_groups = all_record_groups[
    all_record_groups["copies"] > 1
].copy()
duplicate_groups["extra_copies"] = (
    duplicate_groups["copies"] - 1
)
duplicate_group_count = len(duplicate_groups)
rows_in_duplicate_groups = int(
    duplicate_groups["copies"].sum()
)
extra_duplicate_rows = int(
    duplicate_groups["extra_copies"].sum()
)
print("Duplicate groups:", duplicate_group_count)
print("Rows in duplicate groups:", rows_in_duplicate_groups)
print("Extra repeated rows:", extra_duplicate_rows)
print("\nTop 15 duplicate groups:")
if not duplicate_groups.empty:
    print(
        duplicate_groups.sort_values(
            "copies", ascending=False
        ).head(15).to_string(index=False)
    )
else:
    print("No duplicate groups found.")

# ============================================================

# SECTION 17: DUPLICATES BY INVOICE

# ============================================================

print("\n" + "=" * 70)
print("17. DUPLICATES BY INVOICE")
print("=" * 70)
if not duplicate_groups.empty:
    invoice_duplicate_summary = (
        duplicate_groups.groupby(
            "InvoiceNo", dropna=False
        )
        .agg(
            duplicate_groups=("copies", "size"),
            extra_duplicate_rows=("extra_copies", "sum"),
            highest_copies_in_one_group=("copies", "max")
        )
        .sort_values("extra_duplicate_rows", ascending=False)
    )
    print("Top 15 invoices with extra duplicate rows:")
    print(invoice_duplicate_summary.head(15).to_string())
    print("\nDuplicate group size distribution:")
    print(
        duplicate_groups["copies"]
        .value_counts()
        .sort_index()
        .rename_axis("identical_copies")
        .to_string()
    )
else:
    invoice_duplicate_summary = pd.DataFrame(
        columns=[
            "duplicate_groups",
            "extra_duplicate_rows",
            "highest_copies_in_one_group"
        ]
    )
    print("No duplicate invoices to summarise.")

# ============================================================

# SECTION 18: DUPLICATE GROUP CHARACTERISTICS

# ============================================================

print("\n" + "=" * 70)
print("18. DUPLICATE GROUP CHARACTERISTICS")
print("=" * 70)
if not duplicate_groups.empty:
    duplicate_groups["is_cancellation"] = (
        duplicate_groups["InvoiceNo"]
        .astype("string")
        .str.startswith("C", na=False)
    )
    duplicate_groups["has_negative_quantity"] = (
        duplicate_groups["Quantity"] < 0
    )
    duplicate_groups["has_zero_price"] = (
        duplicate_groups["UnitPrice"] == 0
    )
    duplicate_groups["has_missing_customer_id"] = (
        duplicate_groups["CustomerID"].isna()
    )
    duplicate_groups["has_missing_description"] = (
        duplicate_groups["Description"].isna()
    )
    duplicate_categories = {
        "Cancellation invoices": "is_cancellation",
        "Negative quantity": "has_negative_quantity",
        "Zero price": "has_zero_price",
        "Missing CustomerID": "has_missing_customer_id",
        "Missing Description": "has_missing_description"
    }
    for category_name, flag_column in duplicate_categories.items():
        matching_groups = duplicate_groups[
            duplicate_groups[flag_column]
        ]
        print(f"\n{category_name}")
        print("Duplicate groups:", len(matching_groups))
        print(
            "Rows in these groups:",
            int(matching_groups["copies"].sum())
        )
        print(
            "Extra repeated rows:",
            int(matching_groups["extra_copies"].sum())
        )
    print(
        "\nNote: these categories can overlap. "
        "They are not automatic deletion rules."
    )
else:
    print("No duplicate groups found.")

# ============================================================

# SECTION 19: INVESTIGATE OTHER HIGH-DUPLICATE INVOICES

# ============================================================

print("\n" + "=" * 70)
print("19. OTHER HIGH-DUPLICATE INVOICES")
print("=" * 70)
if not invoice_duplicate_summary.empty:
    other_invoice_summary = invoice_duplicate_summary[
        invoice_duplicate_summary.index.astype("string")
        != target_invoice
    ]
    top_other_invoices = other_invoice_summary.head(3).index
    for invoice_no in top_other_invoices:
        invoice_text = str(invoice_no)
        invoice_rows = cleaned_df[
            cleaned_df["InvoiceNo"].astype("string")
            == invoice_text
        ].copy()
        invoice_rows = invoice_rows.sort_values(
            "StockCode",
            key=lambda column: column.astype("string")
        )
        print("\n" + "-" * 70)
        print("Invoice:", invoice_text)
        print("Total rows in invoice:", len(invoice_rows))
        invoice_rows.insert(
            0,
            "working_row_position",
            invoice_rows.index
        )
        print(invoice_rows.head(40).to_string(index=False))
else:
    print("No duplicate invoice groups available for investigation.")

# ============================================================

# SECTION 20: INDEPENDENT DUPLICATE VALIDATION

# ============================================================

print("\n" + "=" * 70)
print("20. INDEPENDENT DUPLICATE VALIDATION")
print("=" * 70)
pandas_duplicate_count = int(
    cleaned_df.duplicated(
        subset=original_columns,
        keep="first"
    ).sum()
)
print("Original rows:", len(original_df))
print("Prepared rows:", len(cleaned_df))
print("Duplicate groups:", duplicate_group_count)
print("Rows in duplicate groups:", rows_in_duplicate_groups)
print("Extra repeated rows from groups:", extra_duplicate_rows)
print("Independent Pandas duplicate count:", pandas_duplicate_count)
assert extra_duplicate_rows == pandas_duplicate_count, (
    "Duplicate group totals do not match Pandas."
)
assert original_df.equals(df), (
    "Original dataset was modified."
)
print("Duplicate totals verified successfully.")

# ============================================================

# SECTION 21: DATA QUALITY REVIEW

# ============================================================

print("\n" + "=" * 70)
print("21. DATA QUALITY REVIEW")
print("=" * 70)
quality_review = pd.DataFrame({
    "Issue": [
        "Missing Description",
        "Missing CustomerID",
        "Exact duplicate extra rows after trimming",
        "Negative Quantity",
        "Zero UnitPrice",
        "Negative UnitPrice",
        "C-prefixed invoice rows"
    ],
    "Count": [
        int(cleaned_df["Description"].isna().sum()),
        int(cleaned_df["CustomerID"].isna().sum()),
        int(cleaned_df.duplicated(subset=original_columns).sum()),
        int((cleaned_df["Quantity"] < 0).sum()),
        int((cleaned_df["UnitPrice"] == 0).sum()),
        int((cleaned_df["UnitPrice"] < 0).sum()),
        int(
            cleaned_df["InvoiceNo"]
            .astype("string")
            .str.startswith("C", na=False)
            .sum()
        )
    ]
})
print(quality_review.to_string(index=False))
print("\nCleaning decisions:")
print("- Keep the original dataset unchanged.")
print("- Preserve rows with missing CustomerID.")
print("- Investigate missing descriptions before deciding what to do.")
print("- Preserve returns and cancellation records for net-sales analysis.")
print("- Investigate unusual prices instead of deleting them automatically.")

# ============================================================

# SECTION 22: PREPARE THE ANALYSIS DATASET

# ============================================================

print("\n" + "=" * 70)
print("22. PREPARE ANALYSIS DATASET")
print("=" * 70)
analysis_df = cleaned_df.copy(deep=True)
rows_before_deduplication = len(analysis_df)
# Remove exact repeated records after text trimming.
# Keep the first occurrence of each identical record.

analysis_df = analysis_df.drop_duplicates(
    subset=original_columns,
    keep="first"
).copy()
rows_after_deduplication = len(analysis_df)
rows_removed = (
    rows_before_deduplication - rows_after_deduplication
)
analysis_df = analysis_df.reset_index(drop=True)
print("Rows before duplicate removal:", rows_before_deduplication)
print("Rows after duplicate removal:", rows_after_deduplication)
print("Rows removed:", rows_removed)
print(
    "Remaining duplicate rows:",
    int(analysis_df.duplicated(subset=original_columns).sum())
)
print("Original dataset unchanged:", original_df.equals(df))
assert analysis_df.duplicated(
    subset=original_columns
).sum() == 0
assert len(analysis_df) <= len(original_df)
assert original_df.equals(df)

# ============================================================

# SECTION 23: FINAL CLEAN DATASET VALIDATION

# ============================================================

print("\n" + "=" * 70)
print("23. CLEAN DATASET VALIDATION")
print("=" * 70)
print("Original dataset shape:", original_df.shape)
print("Analysis dataset shape:", analysis_df.shape)
print("\nMissing values in analysis dataset (original columns):")
print(analysis_df[original_columns].isna().sum().to_string())
print("\nData types:")
print(analysis_df[original_columns].dtypes.to_string())
print("\nRemaining exact duplicate rows:", int(analysis_df.duplicated(subset=original_columns).sum()))
print("Original dataset unchanged:", original_df.equals(df))
print("\nNote: duplicate removal is based on the original eight columns " "after trimming outer text spaces.")

# ============================================================

# SECTION 24: FEATURE ENGINEERING

# ============================================================

print("\n" + "=" * 70)
print("24. FEATURE ENGINEERING")
print("=" * 70)
analysis_df["InvoiceDate"] = pd.to_datetime(analysis_df["InvoiceDate"], errors="coerce")
analysis_df["Quantity"] = pd.to_numeric(analysis_df["Quantity"], errors="coerce")
analysis_df["UnitPrice"] = pd.to_numeric(analysis_df["UnitPrice"], errors="coerce")
analysis_df["CustomerID"] = pd.to_numeric(analysis_df["CustomerID"], errors="coerce")
# Nullable integer: keeps missing CustomerIDs as missing values.

analysis_df["CustomerID"] = analysis_df["CustomerID"].astype("Int64")
# Validate numeric conversions before changing CustomerID to Int64.

print("\nNUMERIC CONVERSION VALIDATION")
print(
    "Missing or invalid Quantity:",
    int(analysis_df["Quantity"].isna().sum())
)
print(
    "Missing or invalid UnitPrice:",
    int(analysis_df["UnitPrice"].isna().sum())
)
invalid_customer_ids = (analysis_df["CustomerID"].notna() & ((analysis_df["CustomerID"] % 1 != 0) | (analysis_df["CustomerID"] <= 0)))
print( "Invalid non-missing CustomerIDs:",int(invalid_customer_ids.sum()))
# Transaction line value includes positive and negative transactions.

analysis_df["line_value"] = (analysis_df["Quantity"] * analysis_df["UnitPrice"])
# Date features

analysis_df["year"] = analysis_df["InvoiceDate"].dt.year
analysis_df["month"] = analysis_df["InvoiceDate"].dt.month
analysis_df["month_name"] = analysis_df["InvoiceDate"].dt.strftime("%B")
analysis_df["day_of_week"] = analysis_df["InvoiceDate"].dt.day_name()
analysis_df["hour"] = analysis_df["InvoiceDate"].dt.hour
analysis_df["is_weekend"] = (analysis_df["InvoiceDate"].dt.dayofweek >= 5)
# Transaction flags

analysis_df["is_cancellation"] = (
    analysis_df["InvoiceNo"]
    .astype("string")
    .str.startswith("C", na=False)
)
analysis_df["is_negative_quantity"] = (
    analysis_df["Quantity"] < 0
)
analysis_df["is_zero_price"] = (
    analysis_df["UnitPrice"] == 0
)
analysis_df["is_negative_price"] = (
    analysis_df["UnitPrice"] < 0
)
analysis_df["has_customer_id"] = (
    analysis_df["CustomerID"].notna()
)
# Positive-sales metric:
# Includes positive quantity and price, excluding C-prefixed invoices.
# This is an analysis metric, not verified accounting revenue.

positive_sales_mask = ((analysis_df["Quantity"] > 0) & (analysis_df["UnitPrice"] > 0) & (~analysis_df["is_cancellation"]))
analysis_df["positive_sales_value"] = np.where(positive_sales_mask, analysis_df["Quantity"] * analysis_df["UnitPrice"],0)
print("Feature engineering completed.")
print("Analysis dataset shape:", analysis_df.shape)
new_features = [
    "line_value", "year", "month", "month_name",
    "day_of_week", "hour", "is_weekend",
    "is_cancellation", "is_negative_quantity",
    "is_zero_price", "is_negative_price",
    "has_customer_id", "positive_sales_value"
]
print("\nSample engineered features:")
print(
    analysis_df[new_features].head(10).to_string(index=False)
)

# ============================================================

# SECTION 25: OVERALL BUSINESS KPIs

# ============================================================

print("\n" + "=" * 70)
print("25. OVERALL BUSINESS KPIs")
print("=" * 70)
valid_dates_df = analysis_df[
    analysis_df["InvoiceDate"].notna()
]
unique_invoices = analysis_df["InvoiceNo"].nunique(dropna=True)
unique_customers = analysis_df["CustomerID"].nunique(dropna=True)
unique_products = analysis_df["StockCode"].nunique(dropna=True)
total_quantity = analysis_df["Quantity"].sum()
net_transaction_value = analysis_df["line_value"].sum()
positive_sales_value = analysis_df["positive_sales_value"].sum()
cancellation_rows = int(analysis_df["is_cancellation"].sum())
negative_quantity_rows = int(
    analysis_df["is_negative_quantity"].sum()
)
zero_price_rows = int(analysis_df["is_zero_price"].sum())
missing_customer_rows = int(
    analysis_df["CustomerID"].isna().sum()
)
print("Rows in analysis dataset:", len(analysis_df))
print("Unique invoices:", unique_invoices)
print("Unique customers with an ID:", unique_customers)
print("Unique product codes:", unique_products)
print("Total quantity, including negative quantities:", total_quantity)
print("Net transaction value:", round(net_transaction_value, 2))
print("Positive sales value:", round(positive_sales_value, 2))
print("C-prefixed invoice rows:", cancellation_rows)
print("Negative quantity rows:", negative_quantity_rows)
print("Zero-price rows:", zero_price_rows)
print("Rows missing CustomerID:", missing_customer_rows)
if not valid_dates_df.empty:
    print("First transaction:", valid_dates_df["InvoiceDate"].min())
    print("Last transaction:", valid_dates_df["InvoiceDate"].max())

# ============================================================

# SECTION 26: MONTHLY SALES ANALYSIS

# ============================================================

print("\n" + "=" * 70)
print("26. MONTHLY SALES ANALYSIS")
print("=" * 70)
monthly_source = analysis_df.dropna(subset=["InvoiceDate"]).copy()
monthly_source["sales_month"] = (monthly_source["InvoiceDate"].dt.to_period("M").astype(str))
monthly_sales = (monthly_source.groupby("sales_month", as_index=False).agg(net_transaction_value=("line_value", "sum"), positive_sales_value=("positive_sales_value", "sum"), total_quantity=("Quantity", "sum"), invoice_count=("InvoiceNo", "nunique"), transaction_rows=("InvoiceNo", "size")).sort_values("sales_month").reset_index(drop=True))
monthly_sales[
    ["net_transaction_value", "positive_sales_value"]
] = monthly_sales[
    ["net_transaction_value", "positive_sales_value"]
].round(2)
print(monthly_sales.to_string(index=False))
if not monthly_sales.empty:
    best_month = monthly_sales.loc[
        monthly_sales["positive_sales_value"].idxmax()
    ]
    print("\nMonth with the highest positive sales value:")
    print(best_month.to_string())

# Month-over-Month (MoM) Sales Growth
monthly_sales["previous_month_sales"] = (
    monthly_sales["positive_sales_value"].shift(1)
)

monthly_sales["mom_change"] = (
    monthly_sales["positive_sales_value"]
    - monthly_sales["previous_month_sales"]
)

monthly_sales["mom_growth_pct"] = (
    monthly_sales["mom_change"]
    .div(monthly_sales["previous_month_sales"].replace(0, float("nan")))
    * 100
)

print("\nMonth-over-Month Sales Growth:")
print(
    monthly_sales[
        [
            "sales_month",
            "positive_sales_value",
            "previous_month_sales",
            "mom_change",
            "mom_growth_pct",
        ]
    ].round(2).to_string(index=False)
)


# ============================================================

# SECTION 27: COUNTRY PERFORMANCE

# ============================================================

print("\n" + "=" * 70)
print("27. COUNTRY PERFORMANCE")
print("=" * 70)
country_sales = (
    analysis_df.groupby(
        "Country", dropna=False, as_index=False
    )
    .agg(
        positive_sales_value=("positive_sales_value", "sum"),
        net_transaction_value=("line_value", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        quantity_sold=("Quantity", "sum"),
        customer_count=("CustomerID", "nunique")
    )
    .sort_values("positive_sales_value", ascending=False)
    .reset_index(drop=True)
)
country_sales[
    ["positive_sales_value", "net_transaction_value"]
] = country_sales[
    ["positive_sales_value", "net_transaction_value"]
].round(2)
print("Top 15 countries by positive sales value:")
print(country_sales.head(15).to_string(index=False))
print("\nUnique countries:", analysis_df["Country"].nunique())

# Country contribution to total positive sales
country_sales["sales_contribution_pct"] = (
    country_sales["positive_sales_value"]
    / country_sales["positive_sales_value"].sum()
) * 100

country_sales = country_sales.sort_values(
    "positive_sales_value", ascending=False
).reset_index(drop=True)

print("\nCountry Sales Contribution (%):")
print(
    country_sales[
        ["Country", "positive_sales_value", "sales_contribution_pct"]
    ].head(10).round(2).to_string(index=False)
)

# ============================================================

# SECTION 28: PRODUCT PERFORMANCE

# ============================================================

print("\n" + "=" * 70)
print("28. PRODUCT PERFORMANCE")
print("=" * 70)
product_source = analysis_df[
    (analysis_df["Quantity"] > 0)
    & (analysis_df["UnitPrice"] > 0)
    & (~analysis_df["is_cancellation"])
].copy()
product_performance = (
    product_source.groupby(
        ["StockCode", "Description"],
        dropna=False,
        as_index=False
    )
    .agg(
        quantity_sold=("Quantity", "sum"),
        positive_sales_value=("positive_sales_value", "sum"),
        invoice_count=("InvoiceNo", "nunique")
    )
    .sort_values("positive_sales_value", ascending=False)
    .reset_index(drop=True)
)
product_performance["positive_sales_value"] = (
    product_performance["positive_sales_value"].round(2)
)
print("Top 15 products by positive sales value:")
print(product_performance.head(15).to_string(index=False))
print("\nTop 15 products by quantity sold:")
top_quantity_products = product_performance.sort_values(
    "quantity_sold", ascending=False
).head(15)
print(top_quantity_products.to_string(index=False))
# Product contribution to total positive sales
product_performance["sales_contribution_pct"] = (
    product_performance["positive_sales_value"]
    / product_performance["positive_sales_value"].sum()
) * 100

print("\nTop 10 Products by Sales Contribution (%):")
print(
    product_performance[
        [
            "StockCode",
            "Description",
            "positive_sales_value",
            "sales_contribution_pct",
        ]
    ].head(10).round(2).to_string(index=False)
)
# Investigate unusually high quantity for StockCode 23843
print("\nInvestigation: PAPER CRAFT, LITTLE BIRDIE")
print(
    analysis_df.loc[
        analysis_df["StockCode"].astype(str).eq("23843"),
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "UnitPrice",
            "line_value",
            "CustomerID",
            "Country",
            "InvoiceDate",
        ],
    ].to_string(index=False)
)

# ============================================================

# SECTION 29: CUSTOMER ANALYSIS

# ============================================================

print("\n" + "=" * 70)
print("29. CUSTOMER ANALYSIS")
print("=" * 70)
customer_source = analysis_df[
    analysis_df["CustomerID"].notna()
].copy()
customer_sales_source = customer_source[
    (customer_source["Quantity"] > 0)
    & (customer_source["UnitPrice"] > 0)
    & (~customer_source["is_cancellation"])
].copy()
customer_summary = (
    customer_sales_source.groupby(
        "CustomerID", as_index=False
    )
    .agg(
        total_spend=("positive_sales_value", "sum"),
        total_quantity=("Quantity", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        first_purchase=("InvoiceDate", "min"),
        last_purchase=("InvoiceDate", "max")
    )
)
customer_summary["total_spend"] = (
    customer_summary["total_spend"].round(2)
)
customer_summary = customer_summary.sort_values(
    "total_spend", ascending=False
).reset_index(drop=True)
print("Top 15 customers by positive sales value:")
print(customer_summary.head(15).to_string(index=False))
# Customer contribution to total positive sales
total_customer_sales = customer_summary["total_spend"].sum()

customer_summary["sales_contribution_pct"] = (
    customer_summary["total_spend"] / total_customer_sales
) * 100

print("\nTop 10 Customers by Sales Contribution (%):")
print(
    customer_summary[
        ["CustomerID", "total_spend", "invoice_count", "sales_contribution_pct"]
    ].head(10).round(2).to_string(index=False)
)
print("\nNumber of customers in summary:", len(customer_summary))

# ============================================================

# SECTION 30: RFM-STYLE CUSTOMER ANALYSIS

# ============================================================

print("\n" + "=" * 70)
print("30. RFM-STYLE CUSTOMER ANALYSIS")
print("=" * 70)
if not customer_sales_source.empty:
    valid_customer_dates = customer_sales_source[
        "InvoiceDate"
    ].dropna()
    if not valid_customer_dates.empty:
        reference_date = (
            valid_customer_dates.max().normalize()
            + pd.Timedelta(days=1)
        )
        rfm_source = customer_sales_source.dropna(
            subset=["InvoiceDate"]
        )
        customer_rfm = (
            rfm_source.groupby("CustomerID")
            .agg(
                recency_days=(
                    "InvoiceDate",
                    lambda dates: (
                        reference_date - dates.max().normalize()
                    ).days
                ),
                frequency=("InvoiceNo", "nunique"),
                monetary=("positive_sales_value", "sum")
            )
            .reset_index()
        )
        customer_rfm["monetary"] = (
            customer_rfm["monetary"].round(2)
        )
        print("Reference date:", reference_date)
        print("\nRFM-style summary sample:")
        print(customer_rfm.head(10).to_string(index=False))
    else:
        customer_rfm = pd.DataFrame(
            columns=[
                "CustomerID", "recency_days",
                "frequency", "monetary"
            ]
        )
        print("No valid dates available for RFM analysis.")
else:
    customer_rfm = pd.DataFrame(
        columns=[
            "CustomerID", "recency_days",
            "frequency", "monetary"
        ]
    )
    print("No qualifying positive customer sales were found.")

# ============================================================

# SECTION 31: CANCELLATION AND RETURN SUMMARY

# ============================================================

print("\n" + "=" * 70)
print("31. CANCELLATION AND RETURN SUMMARY")
print("=" * 70)
invoice_text = analysis_df["InvoiceNo"].astype("string")
analysis_df["invoice_prefix_c"] = (
    invoice_text.str.startswith("C", na=False)
)
cancellation_summary = pd.DataFrame({
    "Metric": [
        "Rows with C-prefixed invoice numbers",
        "Unique C-prefixed invoice numbers",
        "Rows with negative quantities",
        "Rows with negative prices",
        "Rows with zero prices"
    ],
    "Value": [
        int(analysis_df["invoice_prefix_c"].sum()),
        int(
            analysis_df.loc[
                analysis_df["invoice_prefix_c"], "InvoiceNo"
            ].nunique()
        ),
        int((analysis_df["Quantity"] < 0).sum()),
        int((analysis_df["UnitPrice"] < 0).sum()),
        int((analysis_df["UnitPrice"] == 0).sum())
    ]
})
print(cancellation_summary.to_string(index=False))
print(
    "\nC-prefixed invoices, negative quantities and negative prices "
    "are different indicators. Do not treat them as identical."
)

# ============================================================
# SECTION 32: SALES BY DAY AND HOUR
# ============================================================

print("\n" + "=" * 70)
print("32. SALES BY DAY AND HOUR")
print("=" * 70)
dated_analysis = analysis_df.dropna(subset=["InvoiceDate"]).copy()
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_sales = (
    dated_analysis.groupby("day_of_week", as_index=False)
    .agg(
        positive_sales_value=("positive_sales_value", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        quantity_sold=("Quantity", "sum")
    )
)
# Include every weekday, even if a day has no rows.

day_sales = (
    day_sales.set_index("day_of_week")
    .reindex(day_order, fill_value=0)
    .rename_axis("day_of_week")
    .reset_index()
)
day_sales["positive_sales_value"] = (
    day_sales["positive_sales_value"].round(2)
)
print("Sales by day of week:")
print(day_sales.to_string(index=False))
hour_sales = (
    dated_analysis.groupby("hour", as_index=False)
    .agg(
        positive_sales_value=("positive_sales_value", "sum"),
        invoice_count=("InvoiceNo", "nunique"),
        transaction_rows=("InvoiceNo", "size")
    )
    .sort_values("hour")
)
hour_sales["positive_sales_value"] = (
    hour_sales["positive_sales_value"].round(2)
)
print("\nSales by hour:")
print(hour_sales.to_string(index=False))

# ============================================================
# SECTION 33: FINAL VALIDATION AND CSV EXPORT
# ============================================================

print("\n" + "=" * 70)
print("33. FINAL VALIDATION AND CSV EXPORT")
print("=" * 70)
print("Original rows:", len(original_df))
print("Analysis rows:", len(analysis_df))
print("Analysis columns:", len(analysis_df.columns))
print("\nMissing values in analysis dataset:")
print(analysis_df.isna().sum().to_string())
print(
    "\nExact duplicate rows remaining:",
    int(analysis_df.duplicated(subset=original_columns).sum())
)
print("InvoiceDate dtype:", analysis_df["InvoiceDate"].dtype)
print("CustomerID dtype:", analysis_df["CustomerID"].dtype)
print("Original dataset unchanged:", original_df.equals(df))
# Validation before export.

assert original_df.equals(df), (
    "Original dataset was modified!"
)
assert analysis_df.duplicated(
    subset=original_columns
).sum() == 0, "Duplicate rows remain!"
assert len(analysis_df) <= len(original_df), (
    "Analysis dataset has more rows than the original dataset."
)
# Save the CSV beside this Python script.

output_dir = Path(__file__).resolve().parent
# Keep the export separate from analysis_df.

export_df = analysis_df.copy(deep=True)
# Use a consistent date format in the CSV.

export_df["InvoiceDate"] = (
    pd.to_datetime(
        export_df["InvoiceDate"], errors="coerce"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")
)
export_df["CustomerID"] = pd.to_numeric(
    export_df["CustomerID"], errors="coerce"
).astype("Int64")
csv_path = output_dir / "online_retail_cleaned.csv"
export_df.to_csv(
    csv_path,
    index=False,
    na_rep=""
)
print("\nCSV export path:")
print(csv_path)
if not csv_path.exists():
    raise FileNotFoundError("CSV export was not created.")
print("CSV file exists:", csv_path.exists())
print("File size in bytes:", csv_path.stat().st_size)
# Re-import the exported file for independent verification.

check_df = pd.read_csv(csv_path)
print("\nCSV RE-IMPORT VALIDATION")
print("Exported rows:", len(export_df))
print("Re-imported rows:", len(check_df))
print("Exported columns:", len(export_df.columns))
print("Re-imported columns:", len(check_df.columns))
columns_match = (
    list(export_df.columns) == list(check_df.columns)
)
print("Column names match:", columns_match)
assert len(export_df) == len(check_df), (
    "CSV row count mismatch!"
)
assert columns_match, (
    "CSV column names or order do not match!"
)
# Check numeric values after CSV export and re-import.

numeric_columns = [
    "Quantity",
    "UnitPrice",
    "line_value",
    "positive_sales_value"
]
for column in numeric_columns:
    original_values = pd.to_numeric(
        export_df[column], errors="coerce"
    ).to_numpy(dtype=float, na_value=np.nan)
    saved_values = pd.to_numeric(
        check_df[column], errors="coerce"
    ).to_numpy(dtype=float, na_value=np.nan)
    assert np.allclose(
        original_values,
        saved_values,
        equal_nan=True
    ), f"Numeric values differ in column: {column}"
print("Numeric values verified after CSV export.")

# Verify InvoiceDate values after CSV export and re-import
export_dates = pd.to_datetime(
    export_df["InvoiceDate"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)
saved_dates = pd.to_datetime(
    check_df["InvoiceDate"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce")

assert export_dates.equals(saved_dates), (
    "InvoiceDate values differ after CSV export!"
)

# Verify CustomerID values after CSV export and re-import
export_customer_ids = pd.to_numeric(
    export_df["CustomerID"], errors="coerce"
)
saved_customer_ids = pd.to_numeric(
    check_df["CustomerID"], errors="coerce"
)

assert np.allclose(
    export_customer_ids.to_numpy(dtype=float, na_value=np.nan),
    saved_customer_ids.to_numpy(dtype=float, na_value=np.nan),
    equal_nan=True
), "CustomerID values differ after CSV export!"

print("InvoiceDate and CustomerID values verified after CSV export.")

# Final Integrity and Consistency Checks
assert original_df.equals(df), (
    "Original dataset changed during processing!"
)
assert len(analysis_df) == len(export_df), (
    "Analysis and export row counts differ!"
)
print("\n" + "=" * 70)
print("PROJECT DATA PREPARATION COMPLETED")
print("=" * 70)
print("Original dataset preserved.")
print("Text preparation completed.")
print("Duplicate investigation completed.")
print("Analysis features created.")
print("Business analysis completed.")
print("CSV export and validation completed.")
print("\nExported file:", csv_path)
