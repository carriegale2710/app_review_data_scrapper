import pandas as pd

INPUT_FILE = "output/combined_app_reviews.csv"
OUTPUT_FILE = "output/cleaned_app_reviews.csv"

def main():
    print("\n\nCLEANING...\n\n")
    df = pd.read_csv(INPUT_FILE)   # column: text 

    # join title (app store reviews only) with text column into new column
    df["title_and_text"] = (
        df["title"].fillna("").astype(str)  
        + "\n---" + 
        df["text"].fillna("").astype(str) 
        )
        
    # very simple cleaning
    df["clean_text"] = (
        df["title_and_text"]
        .fillna("")  # Replace NaN with empty string
        .str.lower()
        .str.replace(r"http\S+|[^a-z\s]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove short reviews with <10 words
    df["char_count"] = df["clean_text"].str.len()
    df = df.loc[df['char_count'] > 30]

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(OUTPUT_FILE, index=False) # Save the cleaned DataFrame to a new CSV file without the index
    print(f"Saved cleaned reviews to {OUTPUT_FILE}")

    # Display the original and cleaned review text for the first 10 rows
    print(df[["text", "clean_text"]].head(10)) 

if __name__ == "__main__":
    main()

