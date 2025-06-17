import os
import pandas as pd

def get_hr_details(file_path):
    # Read Excel with headers
    dataframe = pd.read_excel(file_path)

    # print(dataframe.head())  # Display the first few rows for debugging

    # Create list of dictionaries
    hr_data = []
    for _, row in dataframe.iterrows():
        hr_data.append({
            "email": row["Email"].strip(),
            "first_name": str(row["First Name"]).strip(),
            "company": str(row["Company"]).strip().upper()
        })

    return hr_data

    # Example usage:
    FILE_NAME = "hr_emails_with_names.xlsx"
    FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)

    print(FILE_PATH)

    hr_emails = get_hr_details(FILE_PATH)
    print(f"Total Emails Found: {len(hr_emails)}\n")

    for entry in hr_emails:
        print(entry)
