import json
import html
from currency_symbols import currency_symbols  # Import currency symbols

# Convert each currency symbol to its HTML entity
currency_html_entities = {name: html.escape(symbol) for name, symbol in currency_symbols.items()}

# Print the results
for name, html_entity in currency_html_entities.items():
    print(f"{name} symbol HTML entity: {html_entity}")

try:
    # Load md_countries.json
    with open('md_countries.json', 'r') as md_file:
        md_countries = json.load(md_file)

    # Load countries.json
    with open('countries.json', 'r') as counties_file:
        counties = json.load(counties_file)

    # Dictionary to map country names to their currency and flag information
    country_info = {county['isoAlpha2'].l: {
        "currency_code": county['currency']['code'],
        "currency_name": county['currency']['name'],
        "currency_symbol": str(county['currency'].get('symbol', ' ')),  # Use space if not found
        "currency_flag": county['flag']
    } for county in counties}

    # List to store the matching country data
    matched_countries = []

    # List to store the unmatched country data
    unmatched_countries = []

    # Iterate over md_countries and find matching names in country_info
    for md_country in md_countries:
        country_name = md_country['name']
        if country_name in country_info:
            # Determine the currency symbol
            currency_symbol = country_info[country_name]['currency_symbol']
            if not currency_symbol or currency_symbol == "False":  # Check if symbol is empty or "False"
                currency_symbol = ""  # Handle as an empty string
            "currency_symbol": html.escape(currency_symbol)
            md_country["currency_code"] =country_info[country_name]['currency_code']
            md_country["currency_name"] =country_info[country_name]['currency_name']
            md_country["currency_symbol"] =country_info[country_name]['currency_symbol']
            md_country["currency_flag"] =country_info[country_name]['currency_flag']

            matched_countries.append(md_country)
        else:
            # Handle unmatched countries with empty currency symbol
            unmatched_country_data = {
                "id": md_country['id'],
                "shortName": md_country.get('shortName', 'N/A'),
                "name": md_country['name'],
                "phoneCode": md_country.get('phoneCode', 'N/A'),
                "zipcodeLength": md_country.get('zipcodeLength', 'N/A'),
                "order": md_country.get('order', 'N/A'),
                "mapName": md_country.get('mapName', 'N/A'),
                "currency_code": "",  # Empty since no currency info is available
                "currency_name": "",
                "currency_symbol": "",  # Set as empty string
                "currency_flag": ""
            }
            unmatched_countries.append(unmatched_country_data)

    # Write the matched data to a JSON file
    with open('country_data2222.json', 'w') as output_file:
        json.dump(matched_countries, output_file, indent=4)

    # Write the unmatched data to a separate JSON file
    with open('unmatched_countries.json', 'w') as unmatched_file:
        json.dump(unmatched_countries, unmatched_file, indent=4)

    print("Data has been successfully stored in country_data2222.json")
    print("Unmatched data has been stored in unmatched_countries.json")

except FileNotFoundError as e:
    print(f"Error: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Print HTML entities for all currency symbols
for name, symbol in currency_symbols.items():
    html_entity = html.escape(symbol) or ' '  # Default to space if symbol is empty
    print(f"{name} symbol HTML entity: {html_entity}")
