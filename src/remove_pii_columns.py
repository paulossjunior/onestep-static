#!/usr/bin/env python3
"""
Remove PII (Personally Identifiable Information) columns from scholarship CSV files
Removes: Phone numbers, CPF, RG, and other personal documents
"""

import csv
from pathlib import Path
from typing import List, Dict


class CSVColumnRemover:
    """Removes specified columns from CSV files."""
    
    def __init__(self, columns_to_remove: List[str]):
        self.columns_to_remove = columns_to_remove
    
    def process_file(self, file_path: Path) -> None:
        """Process a single CSV file to remove columns."""
        print(f"Processing: {file_path.name}")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                print(f"  ⚠ Empty file, skipping")
                return
            
            # Get original fieldnames
            original_fields = reader.fieldnames
            
            # Check which columns exist
            columns_found = [col for col in self.columns_to_remove if col in original_fields]
            
            if not columns_found:
                print(f"  ℹ No columns to remove")
                return
            
            # Create new fieldnames without the columns to remove
            new_fields = [f for f in original_fields if f not in self.columns_to_remove]
            
            print(f"  ✓ Removing columns: {', '.join(columns_found)}")
            print(f"  ✓ Original columns: {len(original_fields)}, New columns: {len(new_fields)}")
        
        # Write back to the same file
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=new_fields)
            writer.writeheader()
            
            for row in rows:
                # Remove the columns from each row
                filtered_row = {k: v for k, v in row.items() if k in new_fields}
                writer.writerow(filtered_row)
        
        print(f"  ✓ File updated successfully")
    
    def process_directory(self, directory: Path) -> None:
        """Process all CSV files in a directory."""
        csv_files = list(directory.glob("*.csv"))
        
        if not csv_files:
            print(f"No CSV files found in {directory}")
            return
        
        print(f"\nFound {len(csv_files)} CSV file(s) to process\n")
        print("=" * 80)
        
        for csv_file in csv_files:
            try:
                self.process_file(csv_file)
                print()
            except Exception as e:
                print(f"  ✗ Error processing {csv_file.name}: {e}")
                print()


def main():
    """Main execution function."""
    print("=" * 80)
    print("REMOVE PII COLUMNS FROM SCHOLARSHIP FILES")
    print("=" * 80)
    
    # Configuration
    SCHOLARSHIPS_DIR = Path("source/scholarships")
    COLUMNS_TO_REMOVE = [
        # Phone numbers
        "CelularOrientado",
        "CelularOrientador",
        "Celular",
        "Telefone",
        "TelefoneOrientado",
        "TelefoneOrientador",
        # CPF and documents
        "CPF",
        "CpfOrientado",
        "CpfOrientador",
        "CPFOrientado",
        "CPFOrientador",
        "RG",
        "RGOrientado",
        "RGOrientador",
        "Documento",
        "DocumentoOrientado",
        "DocumentoOrientador",
        # Email (optional - uncomment if needed)
        # "Email",
        # "EmailOrientado",
        # "EmailOrientador",
    ]
    
    print(f"\nDirectory: {SCHOLARSHIPS_DIR}")
    print(f"Columns to remove: {', '.join(COLUMNS_TO_REMOVE)}")
    
    if not SCHOLARSHIPS_DIR.exists():
        print(f"\n✗ Error: Directory {SCHOLARSHIPS_DIR} does not exist")
        return
    
    # Process files
    remover = CSVColumnRemover(COLUMNS_TO_REMOVE)
    remover.process_directory(SCHOLARSHIPS_DIR)
    
    print("=" * 80)
    print("COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
