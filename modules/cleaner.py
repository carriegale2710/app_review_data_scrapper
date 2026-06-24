import pandas as pd

INPUT_FILE = "output/combined_app_reviews.csv"
OUTPUT_FILE = "output/cleaned_app_reviews.csv"

def main():
    print("\n\nCLEANING...\n\n")
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

    # Display the original and cleaned review text for the first 10 rows
    print(df[["text", "clean_text"]].head(10)) 

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(OUTPUT_FILE, index=False) # Save the cleaned DataFrame to a new CSV file without the index
    print(f"Saved cleaned reviews to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

