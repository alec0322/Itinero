import pandas as pd
import json

# Load data from the Excel file (replace 'cities.xlsx' with your file name)
excel_file = "uscities.xlsx"
df = pd.read_excel(excel_file)

# Convert the DataFrame to a list of dictionaries
city_data = df.to_dict(orient="records")

# Define the output JSON file path (replace 'cities.json' with your desired file name)
output_json_file = "cities.json"

# Save the JSON data to the specified file
with open(output_json_file, "w") as json_file:
    json.dump(city_data, json_file, indent=4)

print(f"JSON data saved to {output_json_file}")