import pandas as pd
from pathlib import Path

def clean_amazon_data(df):
    """Clean and transform Amazon product data."""
    print("\n🔄 Cleaning and transforming Amazon product data...")
    
    # Validate essential columns
    essential_cols = ['asin', 'price']
    missing_essential = [col for col in essential_cols if col not in df.columns]
    if missing_essential:
        raise ValueError(f"Missing essential columns: {missing_essential}")

    # Currency conversion with error handling
    price_cols = ['price', 'listPrice']
    for col in price_cols:
        if col in df.columns:
            try:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(r'[^\d.]', '', regex=True)
                    .astype(float)
                )
                print(f"✅ Converted {col} to numeric format")
                print(f"   - {col} stats: Mean=${df[col].mean():.2f}, Max=${df[col].max():.2f}")
            except Exception as e:
                print(f"⚠️ Failed to convert {col}: {str(e)}")
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # Enhanced category handling
    category_col = 'categoryName'
    if category_col in df.columns:
        df['category'] = (
            df[category_col]
            .str.lower()
            .str.strip()
            .str.replace(r'\s+', ' ', regex=True)  # Clean whitespace
            .fillna('uncategorized')
        )
        df = df.drop(columns=[category_col])  # Remove original column
        print("✅ Standardized product categories")
        print(f"   - Top categories: {df['category'].value_counts().head(5).to_dict()}")
    else:
        print("\n⚠️ Warning: Missing category information!")

    # Best seller conversion
    if 'isBestSeller' in df.columns:
        df['isBestSeller'] = pd.to_numeric(df['isBestSeller'], errors='coerce').fillna(0)
        best_seller_count = df['isBestSeller'].sum()
        print(f"✅ Best sellers: {best_seller_count} products ({best_seller_count/len(df):.1%})")

    # Price categorization with validation
    if 'price' in df.columns:
        df['price_category'] = pd.cut(
            df['price'],
            bins=[-1, 0, 25, 50, 100, 500, 1000, float('inf')],
            labels=['Free', 'Budget', 'Standard', 'Premium', 'Expensive', 'Luxury', 'Ultra Luxury'],
            right=False
        )
        # Handle NA prices
        price_na_count = df['price'].isna().sum()
        if price_na_count > 0:
            df['price_category'] = df['price_category'].cat.add_categories('Unknown').fillna('Unknown')
            print(f"⚠️ Categorized {price_na_count} items with missing prices as 'Unknown'")
        
        print("💰 Price distribution:")
        print(df['price_category'].value_counts(dropna=False))

    # Final validation
    print(f"\n✅ Final dataset validation:")
    print(f"- Total products: {len(df):,}")
    print(f"- Columns: {list(df.columns)}")
    print(f"- Missing values per column:")
    print(df.isna().sum())
    
    return df

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / 'data'
    
    try:
        # Load cleaned Amazon data
        input_path = data_dir / 'cleaned_amazon.csv'
        df = pd.read_csv(input_path)
        print(f"\n📥 Loaded Amazon data: {len(df):,} rows")
        
        # Process data
        df_transformed = clean_amazon_data(df)
        
        # Save transformed data
        output_path = data_dir / 'transformed_amazon.csv'
        df_transformed.to_csv(output_path, index=False)
        print(f"\n💾 Saved transformed data to: {output_path}")
        
    except FileNotFoundError:
        print("\n❌ Error: cleaned_amazon.csv not found!")
        print("   Run extract_ecom.py first to generate cleaned data")
    except Exception as e:
        print(f"\n❌ Transformation failed: {str(e)}")