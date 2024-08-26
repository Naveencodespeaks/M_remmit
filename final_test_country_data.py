# import json
# import html

# # Example Unicode currency symbols
# currency_symbols = {
#     "Afghani": '\u060b',  # Afghan Afghani symbol
#     "Euro": '\u20ac',     # Euro symbol
#     "Dollar": '\u0024',   # Dollar symbol
#     "Yen": '\u00a5',      # Yen symbol
#     "Pound": '\u00a3'     # Pound symbol
# }

# # Convert each currency symbol to its HTML entity
# currency_html_entities = {name: html.escape(symbol) for name, symbol in currency_symbols.items()}

# # Print the results
# for name, html_entity in currency_html_entities.items():
#     print(f"{name} symbol HTML entity: {html_entity}")

# # Load md_countries.json
# with open('md_countries.json', 'r') as md_file:
#     md_countries = json.load(md_file)

# # Load countries.json
# with open('countries.json', 'r') as counties_file:
#     counties = json.load(counties_file)

# # Dictionary to map country names to their currency and flag information
# country_info = {county['name']: {
#     "currency_code": county['currency']['code'],
#     "currency_name": county['currency']['name'],
#     "currency_symbol": county['currency']['symbol'],
#     "currency_flag": county['flag']
# } for county in counties}

# # List to store the matching country data
# matched_countries = []

# # Iterate over md_countries and find matching names in country_info
# for md_country in md_countries:
#     country_name = md_country['name']
#     if country_name in country_info:
#         # Store the matching data in a dictionary with additional fields
#         country_data = {
#             "id": md_country['id'],
#             "shortName": md_country.get('shortName', 'N/A'),
#             "name": md_country['name'],
#             "phoneCode": md_country.get('phoneCode', 'N/A'),
#             "zipcodeLength": md_country.get('zipcodeLength', 'N/A'),
#             "order": md_country.get('order', 'N/A'),
#             "mapName": md_country.get('mapName', 'N/A'),
#             **country_info[country_name]  # Unpack the currency and flag info
#         }
#         # Append to the list
#         matched_countries.append(country_data)

# # Write the matched data to a JSON file
# with open('country_dataeEFGH.json', 'w') as output_file:
#     json.dump(matched_countries, output_file, indent=4)

# print("Data has been successfully stored in country_dataABCD.json")




# import json
# import html

# # Load md_countries.json
# with open('md_countries.json', 'r') as md_file:
#     md_countries = json.load(md_file)

# # Load countries.json
# with open('countries.json', 'r') as counties_file:
#     counties = json.load(counties_file)

# # Dictionary to map country names to their currency and flag information
# country_info = {county['name']: {
#     "currency_code": county['currency']['code'],
#     "currency_name": county['currency']['name'],
#     "currency_symbol": str(county['currency']['symbol']),  # Ensure it's a string
#     "currency_flag": county['flag']
# } for county in counties}

# # List to store the matching country data
# matched_countries = []

# # Iterate over md_countries and find matching names in country_info
# for md_country in md_countries:
#     country_name = md_country['name']
#     if country_name in country_info:
#         # Store the matching data in a dictionary with additional fields
#         country_data = {
#             "id": md_country['id'],
#             "shortName": md_country.get('shortName', 'N/A'),
#             "name": md_country['name'],
#             "phoneCode": md_country.get('phoneCode', 'N/A'),
#             "zipcodeLength": md_country.get('zipcodeLength', 'N/A'),
#             "order": md_country.get('order', 'N/A'),
#             "mapName": md_country.get('mapName', 'N/A'),
#             "currency": {
#                 "currency_code": country_info[country_name]['currency_code'],
#                 "currency_name": country_info[country_name]['currency_name'],
#                 "currency_symbol": html.escape(country_info[country_name]['currency_symbol'])  # Convert to HTML entity
#             },
#             "currency_flag": country_info[country_name]['currency_flag']
#         }
#         # Append to the list
#         matched_countries.append(country_data)

# # Write the matched data to a JSON file
# with open('country_data9876.json', 'w') as output_file:
#     json.dump(matched_countries, output_file, indent=4)

# print("Data has been successfully stored in country_dataABCD.json")

# # Print HTML entities for all currency symbols
# for name, info in country_info.items():
#     print(f"{name} symbol HTML entity: {html.escape(info['currency_symbol'])}")



# import json
# import html

# # Example Unicode currency symbols
# currency_symbols = {
#     "Afghani": '\u060b',  # Afghan Afghani symbol
#     "Euro": '\u20ac',     # Euro symbol
#     "Dollar": '\u0024',   # Dollar symbol
#     "Yen": '\u00a5',      # Yen symbol
#     "Pound": '\u00a3'     # Pound symbol
# }

# # Convert each currency symbol to its HTML entity
# currency_html_entities = {name: html.escape(symbol) for name, symbol in currency_symbols.items()}

# # Print the results
# for name, html_entity in currency_html_entities.items():
#     print(f"{name} symbol HTML entity: {html_entity}")

# try:
#     # Load md_countries.json
#     with open('md_countries.json', 'r') as md_file:
#         md_countries = json.load(md_file)

#     # Load countries.json
#     with open('countries.json', 'r') as counties_file:
#         counties = json.load(counties_file)

#     # Dictionary to map country names to their currency and flag information
#     country_info = {county['name']: {
#         "currency_code": county['currency']['code'],
#         "currency_name": county['currency']['name'],
#         "currency_symbol": str(county['currency'].get('symbol', '')),  # Use empty string if not found
#         "currency_flag": county['flag']
#     } for county in counties}

#     # List to store the matching country data
#     matched_countries = []

#     # Iterate over md_countries and find matching names in country_info
#     for md_country in md_countries:
#         country_name = md_country['name']
#         if country_name in country_info:
#             # Determine the currency symbol
#             currency_symbol = country_info[country_name]['currency_symbol']
#             if not currency_symbol:  # Check if symbol is empty
#                 currency_symbol = "False"

#             # Store the matching data in a dictionary with additional fields
#             country_data = {
#                 "id": md_country['id'],
#                 "shortName": md_country.get('shortName', 'N/A'),
#                 "name": md_country['name'],
#                 "phoneCode": md_country.get('phoneCode', 'N/A'),
#                 "zipcodeLength": md_country.get('zipcodeLength', 'N/A'),
#                 "order": md_country.get('order', 'N/A'),
#                 "mapName": md_country.get('mapName', 'N/A'),
#                 "currency_code": country_info[country_name]['currency_code'],
#                 "currency_name": country_info[country_name]['currency_name'],
#                 "currency_symbol": html.escape(currency_symbol),  # Convert to HTML entity
#                 "currency_flag": country_info[country_name]['currency_flag']
#                 }
#             # Append to the list
#             matched_countries.append(country_data)

#     # Write the matched data to a JSON file
#     with open('country_data1111.json', 'w') as output_file:
#         json.dump(matched_countries, output_file, indent=4)

#     print("Data has been successfully stored in country_data1111.json")

# except FileNotFoundError as e:
#     print(f"Error: {e}")
# except json.JSONDecodeError as e:
#     print(f"Error decoding JSON: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

# # Print HTML entities for all currency symbols
# for name, info in country_info.items():
#     symbol = info['currency_symbol'] if info['currency_symbol'] else ' '  # Default to space if symbol is empty
#     print(f"{name} symbol HTML entity: {html.escape(symbol)}")





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
    country_info = {county['name']: {
        "currency_code": county['currency']['code'],
        "currency_name": county['currency']['name'],
        "currency_symbol": str(county['currency'].get('symbol', ' ')),  # Use space if not found
        "currency_flag": county['flag']
    } for county in counties}

    # List to store the matching country data
    matched_countries = []

    # Iterate over md_countries and find matching names in country_info
    for md_country in md_countries:
        country_name = md_country['name']
        if country_name in country_info:
            # Determine the currency symbol
            currency_symbol = country_info[country_name]['currency_symbol']
            if not currency_symbol:  # Check if symbol is empty
                currency_symbol = ""  # Handle as a space

            # Store the matching data in a dictionary with additional fields
            country_data = {
                "id": md_country['id'],
                "shortName": md_country.get('shortName', 'N/A'),
                "name": md_country['name'],
                "phoneCode": md_country.get('phoneCode', 'N/A'),
                "zipcodeLength": md_country.get('zipcodeLength', 'N/A'),
                "order": md_country.get('order', 'N/A'),
                "mapName": md_country.get('mapName', 'N/A'),
                "currency_code": country_info[country_name]['currency_code'],
                "currency_name": country_info[country_name]['currency_name'],
                "currency_symbol": html.escape(currency_symbol),  # Convert to HTML entity
                "currency_flag": country_info[country_name]['currency_flag']
            }
            md_country["currency_code"] = country_info[country_name]['currency_code']
            # Append to the list
            matched_countries.append(country_data)

    # Write the matched data to a JSON file
    with open('country_data1111.json', 'w') as output_file:
        json.dump(matched_countries, output_file, indent=4)

    print("Data has been successfully stored in country_data1111.json")

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



