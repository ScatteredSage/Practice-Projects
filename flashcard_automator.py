import csv

# 1. Target your exact input file
input_file = "master_cloze_deck.txt"

# 2. Export locally to the same Practice-Projects directory
export_path = "path_to_directory"

try:
    # 3. Read the AI-generated text file
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 4. Parse the Front and Back of the cards
    formatted_cards = []
    for line in lines:
        # Assumes the AI separated the front and back with a colon
        if ":" in line:
            front, back = line.split(":", 1)
            formatted_cards.append([front.strip(), back.strip()])

    # 5. Write the Anki-ready CSV file
    with open(export_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(formatted_cards)

    print(f"Success! Deck saved as {export_path} in your current directory.")

except FileNotFoundError:
    print(f"Error: Could not find {input_file}. Check the spelling.")
except Exception as e:
    print(f"An error occurred: {e}")
