from section_analyzer import SectionAnalyzer, analyze_paper_sections
import json
from pathlib import Path

print('Analyzing sections and extracting insights...')
analyzer = SectionAnalyzer()
sections_dir = Path('data/sections')
analysis_dir = Path('data/section_analysis')
analysis_dir.mkdir(exist_ok=True)

total_papers = 0
total_sections = 0

for sections_file in sections_dir.glob('*_sections.json'):
    paper_name = sections_file.stem.replace('_sections', '')
    print(f'Analyzing: {paper_name}')
    
    try:
        # Use the convenience function
        analysis = analyze_paper_sections(str(sections_file))
        
        if analysis:
            # Save analysis
            analysis_file = analysis_dir / f'{paper_name}_analysis.json'
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            total_papers += 1
            total_sections += len(analysis.get('sections', []))
            
            # Print key insights
            if analysis.get('key_insights'):
                print(f'  Key insights: {len(analysis["key_insights"])} found')
                for insight in analysis['key_insights'][:2]:
                    print(f'    - {insight[:100]}...')
            else:
                print(f'  Sections analyzed: {len(analysis.get("sections", []))}')
        
    except Exception as e:
        print(f'  Error: {e}')

print(f'Analysis completed!')
print(f'Total papers analyzed: {total_papers}')
print(f'Total sections processed: {total_sections}')
