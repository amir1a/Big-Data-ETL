import pandas as pd
from pathlib import Path

def process_amazon_data():
    """Process and analyze Amazon dataset."""
    data_dir = Path(__file__).parent.parent / 'data'
    
    try:
        # Load Amazon dataset
        amazon_df = pd.read_csv(data_dir / 'amazon.csv')
        
        print("📥 Successfully loaded dataset:")
        print(f" - Amazon Products: {len(amazon_df):,} rows")
        print("\n🔍 Initial Data Overview:")
        print(amazon_df.info())

        # Data Cleaning
        print("\n🧹 Performing data cleaning...")
        
        # Remove duplicates based on ASIN (Amazon Standard Identification Number)
        initial_count = len(amazon_df)
        amazon_df = amazon_df.drop_duplicates(subset=['asin'], keep='first')
        print(f"Removed {initial_count - len(amazon_df)} duplicate products")

        # Handle missing values
        print("\n🕵️ Missing Values Before Cleaning:")
        print(amazon_df.isna().sum())

        # Clean price columns
        for col in ['price', 'listPrice']:
            if col in amazon_df.columns:
                # Convert to numeric and handle currency symbols
                amazon_df[col] = pd.to_numeric(
                    amazon_df[col].replace('[\$,]', '', regex=True), 
                    errors='coerce'
                )
                # Fill missing prices with median instead of 0
                amazon_df[col] = amazon_df[col].fillna(amazon_df[col].median())

        # Clean categorical data
        if 'categoryName' in amazon_df.columns:
            amazon_df['categoryName'] = (
                amazon_df['categoryName']
                .str.strip()
                .str.lower()
                .fillna('uncategorized')
            )

        # Save cleaned data
        cleaned_path = data_dir / 'cleaned_amazon.csv'
        amazon_df.to_csv(cleaned_path, index=False)
        print(f"\n✅ Cleaned data saved to: {cleaned_path}")

        # Basic Analysis
        print("\n📊 Basic Data Analysis:")
        if 'price' in amazon_df.columns:
            print(f"Average Price: ${amazon_df['price'].mean():.2f}")
            print(f"Price Range: ${amazon_df['price'].min():.2f} - ${amazon_df['price'].max():.2f}")
            print(f"Median Price: ${amazon_df['price'].median():.2f}")

        if 'stars' in amazon_df.columns:
            print(f"\nAverage Rating: {amazon_df['stars'].mean():.1f}/5")
            print(f"Best Rated: {amazon_df['stars'].max()}/5")
            print(f"Worst Rated: {amazon_df['stars'].min()}/5")
            print(f"Most Common Rating: {amazon_df['stars'].mode()[0]}/5")

        if 'isBestSeller' in amazon_df.columns:
            best_seller_perc = amazon_df['isBestSeller'].mean() * 100
            print(f"\nBest Sellers: {best_seller_perc:.1f}% of products")

        if 'boughtInLastMonth' in amazon_df.columns:
            total_purchases = amazon_df['boughtInLastMonth'].sum()
            print(f"\nTotal purchases last month: {total_purchases:,}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}. Please ensure amazon.csv is in the 'data' directory.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    process_amazon_data()