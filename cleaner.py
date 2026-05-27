import pandas as pd

INPUT_FILE = "combined_app_reviews.csv"
OUTPUT_FILE = "cleaned_app_reviews.csv"

df = pd.read_csv(INPUT_FILE)   # column: text 

# very simple cleaning
df["clean_text"] = (
    df["text"]
    .fillna("")  # Replace NaN with empty string
    .str.lower()
    .str.replace(r"http\S+|[^a-z\s]", "", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print(df[["text", "clean_text"]].head(10)) # Display the original and cleaned review text for the first 10 rows

# Save the cleaned DataFrame to a new CSV file
df.to_csv(OUTPUT_FILE, index=False) # Save the cleaned DataFrame to a new CSV file without the index
print(f"Saved cleaned reviews to {OUTPUT_FILE}")