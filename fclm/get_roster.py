import pandas as pd
from fclm2 import *

# Initialize the FCLM class for HSE1
fclm = FCLM("GYR1")

# Define the parameters to include the additional data in the roster
params = {
    "Photo": "Photo",
    "Employee ID": "Employee ID",
    "User ID": "User ID",
    "Employee Name": "Employee Name",
    "Badge Barcode ID": "Badge Barcode ID",
    "Department ID": "Department ID",
    "Employment Start Date": "Employment Start Date",
    "Employment Type": "Employment Type",
    "Employee Status": "Employee Status",
    "Manager Name": "Manager Name",
    "Temp Agency Code": "Temp Agency Code",
    "Management Area ID": "Management Area ID",
    "Shift Pattern": "Shift Pattern",
    "submit": "true",
}


# Get the current roster
roster = fclm.get_roster()  # Pass the additional parameters to the get_roster method

# If the roster was fetched successfully
if roster is not None:
    # Perform operations on the roster DataFrame
    roster["Employment Start Date"] = pd.to_datetime(roster["Employment Start Date"])
    roster["Date2"] = roster["Employment Start Date"].dt.strftime("%Y-%m-%d")

    # Save the cleaned DataFrame to a CSV file
    roster.to_csv("GYR1_roster.csv", index=False)
