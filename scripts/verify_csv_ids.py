import pandas as pd
import os
import glob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_latest_csv_file():
    """Finds the most recent CSV file in the crawler's output directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'crawler', 'output')
    
    search_pattern = os.path.join(output_dir, '*.csv')
    logging.info(f"Searching for CSV files in: {search_pattern}")
    
    list_of_files = glob.glob(search_pattern)
    if not list_of_files:
        logging.error(f"No CSV files found in {output_dir}")
        raise FileNotFoundError(f"No CSV files matching pattern found in {output_dir}")
        
    latest_file = max(list_of_files, key=os.path.getctime)
    logging.info(f"Found latest CSV file: {latest_file}")
    return latest_file

def verify_data_quality(file_path):
    """Reads a CSV and performs a comprehensive data quality check."""
    logging.info(f"Reading and analyzing file for data quality: {file_path}")
    try:
        df = pd.read_csv(file_path, low_memory=False)
        
        total_rows = len(df)
        logging.info(f"Total rows in CSV: {total_rows}")
        
        if 'listing_id' not in df.columns:
            logging.error("Column 'listing_id' not found in the CSV.")
            return

        # --- ID Verification ---
        if 'listing_id' not in df.columns:
            logging.error("Column 'listing_id' not found in the CSV.")
            return
        null_ids = df['listing_id'].isnull().sum()
        valid_ids = df['listing_id'].dropna()
        duplicates = valid_ids[valid_ids.duplicated(keep=False)]
        num_duplicates = duplicates.nunique()
        total_duplicate_rows = duplicates.count()

        # --- Data Type Coercion Check ---
        # Check rent_pw
        rent_issues = pd.to_numeric(df['rent_pw'], errors='coerce').isnull() & df['rent_pw'].notnull()
        num_rent_issues = rent_issues.sum()

        # Check bedrooms
        bedroom_issues = pd.to_numeric(df['bedrooms'], errors='coerce').isnull() & df['bedrooms'].notnull()
        num_bedroom_issues = bedroom_issues.sum()

        # Check latitude/longitude
        lat_issues = pd.to_numeric(df['latitude'], errors='coerce').isnull() & df['latitude'].notnull()
        lon_issues = pd.to_numeric(df['longitude'], errors='coerce').isnull() & df['longitude'].notnull()
        num_lat_lon_issues = (lat_issues | lon_issues).sum()

        print("\n" + "="*60)
        print("DATA QUALITY & ID VERIFICATION REPORT")
        print("="*60)
        print(f"File Analyzed: {os.path.basename(file_path)}")
        print(f"Total Rows: {total_rows}")
        print("-" * 60)

        print("\n[ID Uniqueness Analysis]")
        print(f"Rows with Null/Empty ID: {null_ids}")
        print(f"Total Unique IDs: {valid_ids.nunique()}")
        if total_duplicate_rows > 0:
            print(f"Found {total_duplicate_rows} rows that are duplicates of {num_duplicates} unique IDs.")
            print("Duplicate IDs and their counts:")
            print(duplicates.value_counts())
        else:
            print("✅ All listing_ids are unique.")
        
        print("\n[Data Format Analysis]")
        print(f"Rows with non-numeric 'rent_pw': {num_rent_issues}")
        if num_rent_issues > 0:
            print("Problematic 'rent_pw' values:")
            print(df[rent_issues]['rent_pw'].value_counts().head())

        print(f"\nRows with non-numeric 'bedrooms': {num_bedroom_issues}")
        if num_bedroom_issues > 0:
            print("Problematic 'bedrooms' values:")
            print(df[bedroom_issues]['bedrooms'].value_counts().head())

        print(f"\nRows with invalid lat/lon coordinates: {num_lat_lon_issues}")
        if num_lat_lon_issues > 0:
            print("Sample of rows with coordinate issues:")
            print(df[lat_issues | lon_issues][['listing_id', 'latitude', 'longitude']].head())

        print("\n" + "="*60)
        
        # Summary of potential data loss
        total_potential_loss = null_ids + total_duplicate_rows - num_duplicates + num_rent_issues + num_bedroom_issues + num_lat_lon_issues
        print(f"\n[Summary of Potential Data Loss]")
        print(f"Duplicate Rows to be Dropped: {total_duplicate_rows - num_duplicates}")
        print(f"Rows with Data Format Issues (rent, bedrooms, coordinates): {num_rent_issues + num_bedroom_issues + num_lat_lon_issues}")
        print(f"Note: A single row can have multiple issues.")
        print("="*60)

    except Exception as e:
        logging.error(f"An error occurred while verifying the CSV: {e}", exc_info=True)

def main():
    """Main function to find the latest CSV and verify it."""
    try:
        latest_csv = find_latest_csv_file()
        verify_data_quality(latest_csv)
    except FileNotFoundError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"An unexpected error occurred in main: {e}")

if __name__ == "__main__":
    main()
