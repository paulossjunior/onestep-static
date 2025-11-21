#!/usr/bin/env python3
"""
Remove CPF and other PII fields from scholarships JSON file
"""

import json
from pathlib import Path


def remove_pii_fields(data, fields_to_remove):
    """Remove PII fields from all scholarship records."""
    
    removed_count = 0
    
    for scholarship in data['scholarships']:
        for field in fields_to_remove:
            if field in scholarship:
                del scholarship[field]
                removed_count += 1
    
    return removed_count


def main():
    """Main function to remove PII fields from JSON."""
    
    print("=" * 80)
    print("REMOVE PII FIELDS FROM SCHOLARSHIPS JSON")
    print("=" * 80)
    
    # Configuration
    json_file = Path('data/scholarships.json')
    fields_to_remove = [
        'student_cpf',
        'advisor_cpf',
        'cpf',
        'student_phone',
        'advisor_phone',
        'phone',
        'student_rg',
        'advisor_rg',
        'rg'
    ]
    
    print(f"\nFile: {json_file}")
    print(f"Fields to remove: {', '.join(fields_to_remove)}")
    
    if not json_file.exists():
        print(f"\n✗ Error: File {json_file} does not exist")
        return
    
    # Load data
    print(f"\nLoading data from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_scholarships = len(data['scholarships'])
    print(f"Total scholarships: {total_scholarships}")
    
    # Check which fields exist
    if data['scholarships']:
        sample = data['scholarships'][0]
        existing_fields = [f for f in fields_to_remove if f in sample]
        
        if existing_fields:
            print(f"\nFields found in data: {', '.join(existing_fields)}")
        else:
            print("\n✓ No PII fields found in data")
            return
    
    # Remove PII fields
    print("\nRemoving PII fields...")
    removed_count = remove_pii_fields(data, fields_to_remove)
    
    if removed_count > 0:
        print(f"✓ Removed {removed_count} field instances")
        
        # Save updated data
        print(f"\nSaving updated data to {json_file}...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✓ File updated successfully!")
    else:
        print("✓ No fields were removed (already clean)")
    
    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
