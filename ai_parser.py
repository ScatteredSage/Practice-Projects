from google import genai

# Initialize the new client with your API key
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# 1. Open our extracted text file in 'read' mode
with open("raw_extracted_notes.txt", "r") as file:
    # Read just the first 3000 characters for our test run
    raw_text = file.read()

# Construct the prompt instruction
prompt = """
Analyze the following Linux study notes. 
Create concrete scenarios and definitions using the Anki Cloze deletion format.
Format every line EXACTLY like this with a pipe character separating the front and back:
Concrete scenario with {{c1::blank}} | Concept First explanation of the underlying system logic.

Here are the notes:
""" + raw_text

print("Sending data to the AI pipeline...")

# 2. Pass our constructed instruction variable to the model using the new syntax
response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents=prompt
)

# 3. Open a new final Anki import file in 'write' mode
with open("master_cloze_deck.txt", "w") as anki_file:
    card_number = ""
    
    # Split the AI's response into individual lines
    for line in response.text.strip().split('\n'):
        # Only process lines that actually contain our pipe separator
        if "|" in line:
            anki_file.write(f"{card_number}. {line}\n")
            card_number += 1

print("AI generation complete. Check master_cloze_deck.txt!")
