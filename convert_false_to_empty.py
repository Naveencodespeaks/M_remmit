import json

try:
    # Load the JSON data from the file
    with open("country_data888.json", "r") as file:
        data = json.load(file)

    # Iterate over each country entry and update currency_symbol
    for country in data:
        if country.get("currency_symbol") == "False":
            country["currency_symbol"] = ""  # Replace "False" with " "

    # Save the updated data to a new file
    with open("final_countries_data_2222.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Replacements completed successfully and data saved to final_countries_data_2222.json.")

except FileNotFoundError as e:
    print(f"Error: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
