# Big-Data-ETL

## How to Run

## Requirements

- Python 3.10+
- PostgreSQL 14+

## Setup
## create env 
python -m venv myenv  
.\myenv\Scripts\Activate.ps1

1. Install dependencies:

   ```bash
   pip install -r requirements.txt

Create .env file
  DB_URL=postgresql://user:password@localhost:5432/ecom

# extract data.rar

# 1. Process raw data

python scripts/extract_ecom.py

# 2.transform

python scripts/transform.py

# 3. Load to database

python scripts/.py

# 4. visualization link
  https://app.powerbi.com/links/H03aoTEOo7?ctid=1695066a-e388-40d1-8ed5-5d0b28ba9f80&pbi_source=linkShare
