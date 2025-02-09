from sqlalchemy import create_engine, exc
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# Simplified loading order based on available data
LOAD_ORDER = ['products', 'categories', 'reviews']

def load_to_postgres():
    """Load transformed Amazon data into PostgreSQL with proper schema relationships."""
    load_dotenv()
    db_url = os.getenv("DB_URL")
    
    if not db_url:
        raise ValueError("❌ DB_URL not found in .env file")

    try:
        engine = create_engine(db_url)
        data_dir = Path(__file__).parent.parent / 'data'
        input_path = data_dir / 'transformed_amazon.csv'
        
        if not input_path.exists():
            raise FileNotFoundError(f"❌ Missing transformed data: {input_path}\nRun transformation step first.")

        print("📥 Loading transformed Amazon data...")
        df = pd.read_csv(input_path)
        
        # Create table DataFrames based on actual data columns
        tables = {
            'products': df[[
                'asin', 'title', 'price', 'listPrice',
                'category', 'isBestSeller', 'boughtInLastMonth',
                'price_category'
            ]].drop_duplicates('asin').rename(columns={
                'asin': 'product_id',
            
                'listPrice': 'list_price'
            }),
            
            'categories': pd.DataFrame({
                'category_name': df['category'].unique()
            }),
            
            'reviews': df[[
                'asin', 'stars', 'reviews'
            ]].rename(columns={
                'asin': 'product_id',
                'stars': 'average_rating',
                'reviews': 'review_count'
            })
        }

        # Load data in proper order
        with engine.begin() as conn:
            for table in LOAD_ORDER:
                if table in tables:
                    print(f"🚚 Loading {table}...")
                    try:
                        tables[table].to_sql(
                            name=table,
                            con=conn,
                            if_exists='replace',
                            index=False,
                            method='multi',
                            chunksize=1000
                        )
                        print(f"✅ Loaded {len(tables[table])} rows to {table}")
                    except exc.SQLAlchemyError as e:
                        print(f"❌ Error loading {table}: {str(e)}")
                        raise

        print("\n🎉 Successfully loaded Amazon product catalog!")

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        raise

if __name__ == "__main__":
    load_to_postgres()