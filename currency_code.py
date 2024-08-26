# # import json

# # with open("countries.json",'r') as file:
# #     data = json.load(file)

# # print(data)



# import json

# # Load md_countries.json
# with open('md_countries.json', 'r') as md_file:
#     md_countries = json.load(md_file)

# # Load counties.json
# with open('countries.json', 'r') as counties_file:
#     counties = json.load(counties_file)

# # Iterate over md_countries and find matching names in counties
# for md_country in md_countries:
#     for county in counties:
#         if md_country['name'] == county['name']:
#             print(f"Country: {md_country['name']}")
#             print(f"Currency Code: {county['currency']['code']}")
#             print(f"Currency Name: {county['currency']['name']}")
#             print(f"Currency Symbol: {county['currency']['symbol']}")
#             print(f"Flag: {county['flag']}")
#             print(f"ISO Alpha-2: {county['isoAlpha2']}")
#             print(f"ISO Alpha-3: {county['isoAlpha3']}")
#             print()


import json

# Load md_countries.json
with open('md_countries.json', 'r') as md_file:
    md_countries = json.load(md_file)

# Load countries.json
with open('countries.json', 'r') as counties_file:
    counties = json.load(counties_file)

# List to store the matching country data
matched_countries = []

# Iterate over md_countries and find matching names in counties
for md_country in md_countries:
    for county in counties:
        if md_country['name'] == county['name']:
            # Store the matching data in a dictionary
            country_data = {
                "Country": md_country['name'],
                "Currency Code": county['currency']['code'],
                "Currency Name": county['currency']['name'],
                "Currency Symbol": county['currency']['symbol'],
                "Flag": county['flag'],
                "ISO Alpha-2": county['isoAlpha2'],
                "ISO Alpha-3": county['isoAlpha3']
            }
            # Append to the list
            matched_countries.append(country_data)

# Write the matched data to a JSON file
with open('country_data.json', 'w') as output_file:
    json.dump(matched_countries, output_file, indent=4)

print("Data has been successfully stored in country_data.json")






