import json
from pathlib import Path

print('Performing simple analysis of extracted sections...')
sections_dir = Path('data/sections')
analysis_dir = Path('data/section_analysis')
analysis_dir.mkdir(exist_ok=True)

total_papers = 0
total_sections = 0
all_section_types = []

for sections_file in sections_dir.glob('*_sections.json'):
    paper_name = sections_file.stem.replace('_sections', '')
    print(f'Analyzing: {paper_name}')
    
    try:
        with open(sections_file, 'r', encoding='utf-8') as f:
            sections_data = json.load(f)
        
        # Simple analysis
        analysis = {
            'paper_name': paper_name,
            'total_sections': len(sections_data),
            'sections': [],
            'section_types': [],
            'total_words': 0,
            'key_insights': []
        }
        
        for section in sections_data:
            section_info = {
                'title': section.get('title', 'Unknown'),
                'type': section.get('section_type', 'unknown'),
                'word_count': section.get('word_count', 0),
                'pages': f"{section.get('start_page', 1)}-{section.get('end_page', 1)}"
            }
            
            analysis['sections'].append(section_info)
            analysis['section_types'].append(section_info['type'])
            analysis['total_words'] += section_info['word_count']
            
            # Extract key insights from abstract
            if section_info['type'] == 'abstract' and len(section.get('content', '')) > 100:
                content = section.get('content', '')
                # Extract first few sentences as insights
                sentences = content.split('. ')
                for sentence in sentences[:2]:
                    if len(sentence) > 50:
                        analysis['key_insights'].append(sentence.strip())
        
        all_section_types.extend(analysis['section_types'])
        
        # Save analysis
        analysis_file = analysis_dir / f'{paper_name}_analysis.json'
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        total_papers += 1
        total_sections += len(sections_data)
        
        print(f'  Sections: {len(sections_data)}')
        print(f'  Words: {analysis["total_words"]}')
        print(f'  Types: {set(analysis["section_types"])}')
        if analysis['key_insights']:
            print(f'  Key insights: {len(analysis["key_insights"])}')
            for insight in analysis['key_insights'][:1]:
                print(f'    - {insight[:100]}...')
        
    except Exception as e:
        print(f'  Error: {e}')

print(f'\nAnalysis completed!')
print(f'Total papers analyzed: {total_papers}')
print(f'Total sections processed: {total_sections}')
print(f'Section types found: {set(all_section_types)}')

# Create a summary report
summary = {
    'total_papers': total_papers,
    'total_sections': total_sections,
    'section_types': list(set(all_section_types)),
    'section_type_counts': {stype: all_section_types.count(stype) for stype in set(all_section_types)}
}

summary_file = analysis_dir / 'summary_report.json'
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f'Summary report saved to: {summary_file}')
