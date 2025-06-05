#!/usr/bin/env python3
"""
Data Setup Script

This script extracts the data files from the ZIP archives in the data directory.
It should be run once after cloning the repository.
"""

import os
import zipfile
import logging
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('setup_data')

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
ZIP_FILES = [
    'ml-latest-small.zip',
    'tmdb_metadata.zip'
]

def extract_zip(zip_path, extract_to):
    """Extract a ZIP file to the specified directory."""
    try:
        # First try with Python's zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Successfully extracted {zip_path}")
        return True
    except zipfile.BadZipFile:
        # If that fails, try using the system's unzip command
        logger.warning(f"Python zipfile failed for {zip_path}, trying system unzip...")
        try:
            import subprocess
            result = subprocess.run(['unzip', '-o', str(zip_path), '-d', str(extract_to)], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Successfully extracted {zip_path} using system unzip")
                return True
            else:
                logger.error(f"System unzip failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Failed to extract {zip_path} using system unzip: {e}")
            return False
    except Exception as e:
        logger.error(f"Failed to extract {zip_path}: {e}")
        return False

def main():
    """Main function to extract all ZIP files."""
    logger.info("Starting data extraction process")
    
    # Create data directory if it doesn't exist
    if not DATA_DIR.exists():
        logger.info(f"Creating data directory: {DATA_DIR}")
        DATA_DIR.mkdir(parents=True)
    
    # Extract each ZIP file
    success_count = 0
    for zip_file in ZIP_FILES:
        zip_path = DATA_DIR / zip_file
        if zip_path.exists():
            # Remove existing directory if it exists (to ensure clean extraction)
            dir_name = zip_file.replace('.zip', '')
            dir_path = DATA_DIR / dir_name
            if dir_path.exists() and dir_path.is_dir():
                logger.info(f"Removing existing directory: {dir_path}")
                shutil.rmtree(dir_path)
            
            if extract_zip(zip_path, DATA_DIR):
                success_count += 1
        else:
            logger.warning(f"ZIP file not found: {zip_path}")
    
    # Report results
    if success_count == len(ZIP_FILES):
        logger.info("All data files extracted successfully")
    else:
        logger.warning(f"Extracted {success_count}/{len(ZIP_FILES)} data files")
    
    logger.info("Data setup complete")

if __name__ == "__main__":
    main() 