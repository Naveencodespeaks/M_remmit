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

# Function to convert any Unicode characters in a string to HTML entities
def convert_to_html_entities(text):
    return ''.join(f'&#{ord(char)};' if ord(char) > 127 else char for char in text)

# Merge data
merged_data = []
for md_country in md_countries_data:
    isoAlpha2 = md_country['shortName']
    country = find_country_by_isoAlpha2(isoAlpha2, countries_data)

    if country:
        currency_symbol = country['currency'].get('symbol', '')

        # Ensure currency_symbol is a string and convert it if necessary
        if isinstance(currency_symbol, str):
            # Convert to HTML entities if it contains any Unicode characters
            currency_symbol_html = convert_to_html_entities(currency_symbol)
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
            "currencyCode": country['currency'].get('code', ''),
            "currency_name": country['currency'].get('name', ''),
            "currencySymbol": currency_symbol_html,
            "flag": country.get('flag', '')
        }
        merged_data.append(merged_entry)

# Write the merged data to a new JSON file
with open('html_entities_4.json', 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print("Data merged and written to html_entities_3.json")
