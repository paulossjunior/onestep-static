#!/usr/bin/env python3
"""
Calculate student recurrence statistics for IC scholarships.
This script analyzes how many times each student participated in IC programs.
"""

import json
from collections import defaultdict
from pathlib import Path


def calculate_student_recurrence(scholarships, campus='Serra'):
    """Calculate student participation recurrence statistics."""
    
    # Filter by campus and remove duplicates
    seen_ids = set()
    filtered_scholarships = []
    for s in scholarships:
        if s.get('execution_campus') == campus and s.get('id') not in seen_ids:
            seen_ids.add(s.get('id'))
            filtered_scholarships.append(s)
    
    # Count participations per student
    student_participations = defaultdict(lambda: {'total': 0, 'bolsista': 0, 'voluntario': 0})
    
    for s in filtered_scholarships:
        student = s.get('student', '').strip()
        if not student:
            continue
        
        student_participations[student]['total'] += 1
        
        modality = s.get('modality', '')
        if modality == 'Bolsista':
            student_participations[student]['bolsista'] += 1
        elif modality == 'Voluntário':
            student_participations[student]['voluntario'] += 1
    
    # Calculate distributions
    participation_dist = defaultdict(int)
    bolsista_dist = defaultdict(int)
    voluntario_dist = defaultdict(int)
    
    only_bolsista = 0
    only_voluntario = 0
    mixed_students = 0
    
    for student, counts in student_participations.items():
        # Total participations distribution
        participation_dist[counts['total']] += 1
        
        # Bolsista distribution
        if counts['bolsista'] > 0:
            bolsista_dist[counts['bolsista']] += 1
        
        # Voluntário distribution
        if counts['voluntario'] > 0:
            voluntario_dist[counts['voluntario']] += 1
        
        # Student profiles
        if counts['bolsista'] > 0 and counts['voluntario'] > 0:
            mixed_students += 1
        elif counts['bolsista'] > 0:
            only_bolsista += 1
        elif counts['voluntario'] > 0:
            only_voluntario += 1
    
    return {
        'total_unique_students': len(student_participations),
        'total_scholarships': len(filtered_scholarships),
        'student_profiles': {
            'only_bolsista': only_bolsista,
            'only_voluntario': only_voluntario,
            'mixed': mixed_students
        },
        'participation_distribution': dict(sorted(participation_dist.items())),
        'bolsista_distribution': dict(sorted(bolsista_dist.items())),
        'voluntario_distribution': dict(sorted(voluntario_dist.items()))
    }


def main():
    """Main function to calculate and save student recurrence statistics."""
    
    # Load scholarships data
    data_file = Path('data/scholarships.json')
    print(f"Loading data from {data_file}...")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    scholarships = data['scholarships']
    print(f"Total scholarships in file: {len(scholarships)}")
    
    # Calculate statistics for Serra campus
    print("\nCalculating student recurrence statistics for Campus Serra...")
    stats = calculate_student_recurrence(scholarships, campus='Serra')
    
    # Print summary
    print(f"\n{'='*60}")
    print("STUDENT RECURRENCE STATISTICS - CAMPUS SERRA")
    print(f"{'='*60}")
    print(f"Total unique students: {stats['total_unique_students']}")
    print(f"Total scholarships: {stats['total_scholarships']}")
    print(f"\nStudent Profiles:")
    print(f"  Only Bolsista: {stats['student_profiles']['only_bolsista']}")
    print(f"  Only Voluntário: {stats['student_profiles']['only_voluntario']}")
    print(f"  Mixed (both): {stats['student_profiles']['mixed']}")
    print(f"\nParticipation Distribution:")
    for count, students in stats['participation_distribution'].items():
        print(f"  {count} IC(s): {students} students")
    print(f"\nBolsista Distribution:")
    for count, students in stats['bolsista_distribution'].items():
        print(f"  {count} bolsa(s): {students} students")
    print(f"\nVoluntário Distribution:")
    for count, students in stats['voluntario_distribution'].items():
        print(f"  {count} voluntário(s): {students} students")
    print(f"{'='*60}\n")
    
    # Add statistics to data
    if 'statistics' not in data:
        data['statistics'] = {}
    
    data['statistics']['student_recurrence_serra'] = stats
    
    # Save updated data
    print(f"Saving updated data to {data_file}...")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✓ Student recurrence statistics calculated and saved successfully!")
    print(f"\nStatistics added to: data['statistics']['student_recurrence_serra']")


if __name__ == '__main__':
    main()
