# import json
# import html


# # Load the data from the JSON files
# with open('countries.json', 'r', encoding='utf-8') as f:
#     countries = json.load(f)

# with open('md_countries.json', 'r', encoding='utf-8') as f:
#     md_countries = json.load(f)

# # Create a dictionary to store the merged data
# merged_countries = []

# # Loop through md_countries and match with countries.json by isoAlpha2/shortName
# for md_country in md_countries:
#     short_name = md_country['shortName']
    
#     # Find the matching entry in countries.json
#     matching_country = next((country for country in countries if country['isoAlpha2'] == short_name), None)
    
#     if matching_country:
#         # Create the merged country data
#         merged_country = {
#             "id": md_country.get("id", ""),
#             "shortName": md_country.get("shortName", ""),
#             "name": md_country.get("name", ""),
#             "phoneCode": md_country.get("phoneCode", ""),
#             "zipcodeLength": md_country.get("zipcodeLength", ""),
#             "order": md_country.get("order", ""),
#             "mapName": md_country.get("mapName", ""),
#             "currency_code": matching_country.get("currency", {}).get("code", ""),
#             "currency_name": matching_country.get("currency", {}).get("name", ""),
#             "currency_symbol": matching_country.get("currency", {}).get("symbol", ""),
#             "currency_flag": matching_country.get("flag", "")
#         }
        
#         # Append the merged data to the list
#         merged_countries.append(merged_country)

# # Save the merged data to a new JSON file
# with open('2_merged_countries.json', 'w', encoding='utf-8') as f:
#     json.dump(merged_countries, f, ensure_ascii=False, indent=4)

# print("Merged JSON file created successfully!")


# import json
# import html

# # Load data from JSON files
# with open('countries.json', 'r') as countries_file:
#     countries_data = json.load(countries_file)

# with open('md_countries.json', 'r') as md_countries_file:
#     md_countries_data = json.load(md_countries_file)

# # Function to find country by isoAlpha2 code
# def find_country_by_isoAlpha2(isoAlpha2, countries_data):
#     for country in countries_data:
#         if country['isoAlpha2'] == isoAlpha2:
#             return country
#     return None

# # Merge data
# merged_data = []
# for md_country in md_countries_data:
#     isoAlpha2 = md_country['shortName']
#     country = find_country_by_isoAlpha2(isoAlpha2, countries_data)

#     if country:
#         currency_symbol = country['currency'].get('symbol', '')
#         # Convert currency symbol to HTML entity
#         currency_symbol_html = html.escape(currency_symbol) if currency_symbol else ''
        
#         merged_entry = {
#             "id": md_country['id'],
#             "shortName": md_country['shortName'],
#             "name": md_country['name'],
#             "phoneCode": md_country.get('phoneCode', ''),
#             "zipcodeLength": md_country.get('zipcodeLength', ''),  # Default to empty string if key is missing
#             "order": md_country.get('order', ''),
#             "mapName": md_country.get('mapName', ''),
#             "currency_code": country['currency'].get('code', ''),
#             "currency_name": country['currency'].get('name', ''),
#             "currency_symbol": currency_symbol_html,
#             "currency_flag": country.get('flag', '')
#         }
#         merged_data.append(merged_entry)

# # Write the merged data to a new JSON file
# with open('html_entities.json', 'w') as output_file:
#     json.dump(merged_data, output_file, indent=4)

# print("Data merged and written to country_data_with_html_entities.json")



# import json
# import html

# # Load data from JSON files
# with open('countries.json', 'r') as countries_file:
#     countries_data = json.load(countries_file)

# with open('md_countries.json', 'r') as md_countries_file:
#     md_countries_data = json.load(md_countries_file)

# # Function to find country by isoAlpha2 code
# def find_country_by_isoAlpha2(isoAlpha2, countries_data):
#     for country in countries_data:
#         if country['isoAlpha2'] == isoAlpha2:
#             return country
#     return None

# # Merge data
# merged_data = []
# for md_country in md_countries_data:
#     isoAlpha2 = md_country['shortName']
#     country = find_country_by_isoAlpha2(isoAlpha2, countries_data)

#     if country:
#         currency_symbol = country['currency'].get('symbol', '')
#         # Convert currency symbol to HTML entity
#         currency_symbol_html = html.escape(currency_symbol) 
#         if "\u" or "\U"   in currency_symbol:
#             return currency_symbol
            
#         else:
#             currency_symbol_html
        
#         merged_entry = {
#             "id": md_country['id'],
#             "shortName": md_country['shortName'],
#             "name": md_country['name'],
#             "phoneCode": md_country.get('phoneCode', ''),
#             "zipcodeLength": md_country.get('zipcodeLength', ''),  # Default to empty string if key is missing
#             "order": md_country.get('order', ''),
#             "mapName": md_country.get('mapName', ''),
#             "currency_code": country['currency'].get('code', ''),
#             "currency_name": country['currency'].get('name', ''),
#             "currency_symbol": currency_symbol_html,
#             "currency_flag": country.get('flag', '')
#         }
#         merged_data.append(merged_entry)

# # Write the merged data to a new JSON file
# with open('html_entities_1.json', 'w') as output_file:
#     json.dump(merged_data, output_file, indent=4)

# print("Data merged and written to country_data_with_html_entities.json")




import json
import html

# Load data from JSON files
with open('countries.json', 'r') as countries_file:
    countries_data = json.load(countries_file)

with open('md_countries.json', 'r') as md_countries_file:
    md_countries_data = json.load(md_countries_file)

# Function to find country by isoAlpha2 code
def find_country_by_isoAlpha2(isoAlpha2, countries_data):
    for country in countries_data:
        if country['isoAlpha2'] == isoAlpha2:
            return country
    return None

# Merge data
merged_data = []
for md_country in md_countries_data:
    isoAlpha2 = md_country['shortName']
    country = find_country_by_isoAlpha2(isoAlpha2, countries_data)

    if country:
        currency_symbol = country['currency'].get('symbol', '')

        # Ensure currency_symbol is a string
        if isinstance(currency_symbol, str):
            # Check if the currency symbol contains any Unicode characters
            if any(ord(char) > 127 for char in currency_symbol):
                # Convert currency symbol to HTML entity if it's a Unicode character
                currency_symbol_html = html.escape(currency_symbol)
            else:
                currency_symbol_html = currency_symbol  # Use as is if not Unicode
        else:
            currency_symbol_html = ''  # Handle cases where currency_symbol is not a string

        merged_entry = {
            "id": md_country['id'],
            "shortName": md_country['shortName'],
            "name": md_country['name'],
            "phoneCode": md_country.get('phoneCode', ''),
            "zipcodeLength": md_country.get('zipcodeLength', ''),  # Default to empty string if key is missing
            "order": md_country.get('order', ''),
            "mapName": md_country.get('mapName', ''),
            "currency_code": country['currency'].get('code', ''),
            "currency_name": country['currency'].get('name', ''),
            "currency_symbol": currency_symbol_html,
            "currency_flag": country.get('flag', '')
        }
        merged_data.append(merged_entry)

# Write the merged data to a new JSON file
with open('html_entities_2.json', 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print("Data merged and written to html_entities_1.json")

