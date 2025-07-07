import subprocess
import sys
from pathlib import Path

def run_command(command, cwd):
    try:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
    except Exception as e:
        print(f"Error running command {' '.join(command)}: {e}")
        sys.exit(1)

def main():
    print("Starting ETL process...")
    
    # Define paths
    project_root = Path(__file__).parent
    rentalAU_root = project_root / "rentalAU_mcp"
    dist_dir = rentalAU_root / "dist"
    etl_dir = rentalAU_root / "etl"
    
    # Run scraper
    print("\n--- Running scraper ---")
    scraper_command = [sys.executable, "v2.py"]
    run_command(scraper_command, cwd=dist_dir)
    
    # Run database update
    print("\n--- Updating database ---")
    db_update_command = [sys.executable, "update_database.py"]
    run_command(db_update_command, cwd=etl_dir)
    
    print("\nETL process completed.")

if __name__ == "__main__":
    main()
