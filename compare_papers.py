import json
from pathlib import Path
from collections import Counter, defaultdict

print('Performing cross-paper comparison...')
analysis_dir = Path('data/section_analysis')
comparison_dir = Path('data/comparisons')
comparison_dir.mkdir(exist_ok=True)

# Load all analysis files
all_analyses = []
for analysis_file in analysis_dir.glob('*_analysis.json'):
    if analysis_file.name != 'summary_report.json':
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
                all_analyses.append(analysis)
        except Exception as e:
            print(f'Error loading {analysis_file}: {e}')

print(f'Loaded {len(all_analyses)} paper analyses')

# Cross-paper comparison
comparison = {
    'total_papers': len(all_analyses),
    'papers': [],
    'section_type_distribution': {},
    'word_count_stats': {},
    'common_themes': [],
    'section_patterns': {}
}

total_words = 0
all_section_types = []
all_insights = []

for analysis in all_analyses:
    paper_info = {
        'name': analysis['paper_name'],
        'section_count': analysis['total_sections'],
        'word_count': analysis['total_words'],
        'section_types': analysis['section_types']
    }
    comparison['papers'].append(paper_info)
    
    total_words += analysis['total_words']
    all_section_types.extend(analysis['section_types'])
    all_insights.extend(analysis.get('key_insights', []))

# Section type distribution
section_type_counts = Counter(all_section_types)
comparison['section_type_distribution'] = dict(section_type_counts)

# Word count statistics
word_counts = [p['word_count'] for p in comparison['papers']]
comparison['word_count_stats'] = {
    'total_words': total_words,
    'average_words_per_paper': total_words / len(all_analyses) if all_analyses else 0,
    'min_words': min(word_counts) if word_counts else 0,
    'max_words': max(word_counts) if word_counts else 0
}

# Common themes from insights
insight_words = []
for insight in all_insights:
    words = insight.lower().split()
    insight_words.extend([w for w in words if len(w) > 4])

common_themes = Counter(insight_words).most_common(10)
comparison['common_themes'] = [{'theme': theme, 'count': count} for theme, count in common_themes]

# Section patterns
for section_type in section_type_counts:
    papers_with_section = [p for p in comparison['papers'] if section_type in p['section_types']]
    comparison['section_patterns'][section_type] = {
        'paper_count': len(papers_with_section),
        'percentage': (len(papers_with_section) / len(all_analyses)) * 100 if all_analyses else 0
    }

# Save comparison
comparison_file = comparison_dir / 'cross_paper_comparison.json'
with open(comparison_file, 'w', encoding='utf-8') as f:
    json.dump(comparison, f, indent=2, ensure_ascii=False)

print(f'\nCross-Paper Comparison Results:')
print(f'=' * 50)
print(f'Total papers compared: {comparison["total_papers"]}')
print(f'Total words analyzed: {comparison["word_count_stats"]["total_words"]:,}')
print(f'Average words per paper: {comparison["word_count_stats"]["average_words_per_paper"]:,.0f}')
print(f'Word count range: {comparison["word_count_stats"]["min_words"]:,} - {comparison["word_count_stats"]["max_words"]:,}')

print(f'\nSection Type Distribution:')
for section_type, count in sorted(comparison['section_type_distribution'].items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(all_analyses)) * 100
    print(f'  {section_type}: {count} papers ({percentage:.1f}%)')

print(f'\nTop Common Themes:')
for theme_info in comparison['common_themes'][:5]:
    print(f'  {theme_info["theme"]}: {theme_info["count"]} mentions')

print(f'\nComparison saved to: {comparison_file}')

# Generate a summary report
summary = f"""
# Cross-Paper Analysis Summary

## Overview
- **Total Papers Analyzed**: {comparison['total_papers']}
- **Total Words Processed**: {comparison['word_count_stats']['total_words']:,}
- **Average Words per Paper**: {comparison['word_count_stats']['average_words_per_paper']:,.0f}

## Section Distribution
Most common section types across papers:
{chr(10).join([f"- {stype}: {count} papers" for stype, count in sorted(comparison['section_type_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]])}

## Key Insights
- **Total Key Insights Extracted**: {len(all_insights)}
- **Papers with Abstracts**: {comparison['section_patterns'].get('abstract', {}).get('paper_count', 0)}
- **Papers with Introductions**: {comparison['section_patterns'].get('introduction', {}).get('paper_count', 0)}

## Common Research Themes
{chr(10).join([f"- {theme['theme'].title()}: {theme['count']} mentions" for theme in comparison['common_themes'][:5]])}
"""

summary_file = comparison_dir / 'comparison_summary.md'
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f'Summary report saved to: {summary_file}')
