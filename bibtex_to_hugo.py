import bibtexparser
import os
import re
import argparse
from datetime import datetime

def format_authors(authors_string):
    """Convert BibTeX author format to the required output format."""
    authors = authors_string.split(' and ')
    formatted_authors = []
    
    for author in authors:
        parts = author.split(', ')
        if len(parts) == 2:
            # Handle "Lastname, Firstname" format
            formatted_authors.append(f"{parts[0]}, {parts[1][0]}.")
        else:
            # Just use as is if format is different
            formatted_authors.append(author)
    
    if len(formatted_authors) == 1:
        return formatted_authors[0]
    elif len(formatted_authors) == 2:
        return f"{formatted_authors[0]} & {formatted_authors[1]}"
    else:
        return ", ".join(formatted_authors[:-1]) + f", & {formatted_authors[-1]}"

def format_citation(entry):
    """Create citation string from BibTeX entry."""
    authors = format_authors(entry.get('author', ''))
    title = entry.get('title', '').strip('{}')
    journal = entry.get('journal', entry.get('booktitle', ''))
    volume = entry.get('volume', '')
    number = entry.get('number', '')
    pages = entry.get('pages', '').replace('--', '-')
    year = entry.get('year', '')
    
    if journal:
        if volume and number and pages:
            return f"{authors} ({year}). {title}. {journal}, {volume}({number}), {pages}."
        elif volume and pages:
            return f"{authors} ({year}). {title}. {journal}, {volume}, {pages}."
        else:
            return f"{authors} ({year}). {title}. {journal}."
    else:
        return f"{authors} ({year}). {title}."

def format_date(year):
    """Format the date field using the year."""
    try:
        return f"{year}-01-01"
    except:
        return datetime.now().strftime("%Y-%m-%d")

def format_bibtex(entry):
    """Format bibtex entry with consistent structure."""
    entry_type = entry.get('ENTRYTYPE', 'article')
    entry_id = entry.get('ID', '')
    
    # Start with the basic structure
    bibtex_str = f"""  @{entry_type}{{{entry_id},
    title={{{entry.get('title', '')}}},
    author={{{entry.get('author', '')}}},"""

    # Add journal or booktitle
    if 'journal' in entry:
        bibtex_str += f"""
    journal={{{entry.get('journal', '')}}},"""
    elif 'booktitle' in entry:
        bibtex_str += f"""
    booktitle={{{entry.get('booktitle', '')}}},"""
    
    # Add other common fields in a specific order
    for field in ['volume', 'number', 'pages', 'year', 'publisher', 'doi', 'organization']:
        if field in entry:
            bibtex_str += f"""
    {field}={{{entry.get(field, '')}}},"""
    
    # Add any remaining fields
    for key, value in entry.items():
        if key not in ['ENTRYTYPE', 'ID', 'title', 'author', 'journal', 'booktitle', 
                       'volume', 'number', 'pages', 'year', 'publisher', 'doi', 'organization']:
            bibtex_str += f"""
    {key}={{{value}}},"""
    
    # Close the entry
    bibtex_str += """
  }"""
    
    return bibtex_str

def replace_special_characters(text):
    """Replace LaTeX-style special characters with Unicode."""
    # Common LaTeX-style accented characters
    replacements = {
        "{\\\'e}": "é", "{\\\'E}": "É",
        "{\\`e}": "è", "{\\`E}": "È",
        "{\\^e}": "ê", "{\\^E}": "Ê",
        "{\\\"e}": "ë", "{\\\"E}": "Ë",
        
        "{\'e}": "é", "{\'E}": "É",
        "{`e}": "è", "{`E}": "È",
        "{^e}": "ê", "{^E}": "Ê",
        "{\"e}": "ë", "{\"E}": "Ë",
        
        "\\\'e": "é", "\\\'E": "É",
        "\\`e": "è", "\\`E": "È",
        "\\^e": "ê", "\\^E": "Ê",
        "\\\"e": "ë", "\\\"E": "Ë",
        
        # Add more replacements as needed for other characters
        # French
        "{\\\'a}": "á", "{\\\'A}": "Á",
        "{\\`a}": "à", "{\\`A}": "À",
        "{\\^a}": "â", "{\\^A}": "Â",
        "{\\\"a}": "ä", "{\\\"A}": "Ä",
        "{\\\'i}": "í", "{\\\'I}": "Í",
        "{\\`i}": "ì", "{\\`I}": "Ì",
        "{\\^i}": "î", "{\\^I}": "Î",
        "{\\\"i}": "ï", "{\\\"I}": "Ï",
        "{\\\'o}": "ó", "{\\\'O}": "Ó",
        "{\\`o}": "ò", "{\\`O}": "Ò",
        "{\\^o}": "ô", "{\\^O}": "Ô",
        "{\\\"o}": "ö", "{\\\"O}": "Ö",
        "{\\\'u}": "ú", "{\\\'U}": "Ú",
        "{\\`u}": "ù", "{\\`U}": "Ù",
        "{\\^u}": "û", "{\\^U}": "Û",
        "{\\\"u}": "ü", "{\\\"U}": "Ü",
        "{\\c c}": "ç", "{\\c C}": "Ç",
        
        "{\'a}": "á", "{\'A}": "Á",
        "{`a}": "à", "{`A}": "À",
        "{^a}": "â", "{^A}": "Â",
        "{\"a}": "ä", "{\"A}": "Ä",
        "{\'i}": "í", "{\'I}": "Í",
        "{`i}": "ì", "{`I}": "Ì",
        "{^i}": "î", "{^I}": "Î",
        "{\"i}": "ï", "{\"I}": "Ï",
        "{\'o}": "ó", "{\'O}": "Ó",
        "{`o}": "ò", "{`O}": "Ò",
        "{^o}": "ô", "{^O}": "Ô",
        "{\"o}": "ö", "{\"O}": "Ö",
        "{\'u}": "ú", "{\'U}": "Ú",
        "{`u}": "ù", "{`U}": "Ù",
        "{^u}": "û", "{^U}": "Û", 
        "{\"u}": "ü", "{\"U}": "Ü",
        "{c c}": "ç", "{c C}": "Ç",
        
        "\\\'a": "á", "\\\'A": "Á",
        "\\`a": "à", "\\`A": "À",
        "\\^a": "â", "\\^A": "Â",
        "\\\"a": "ä", "\\\"A": "Ä",
        "\\\'i": "í", "\\\'I": "Í",
        "\\`i": "ì", "\\`I": "Ì",
        "\\^i": "î", "\\^I": "Î",
        "\\\"i": "ï", "\\\"I": "Ï",
        "\\\'o": "ó", "\\\'O": "Ó",
        "\\`o": "ò", "\\`O": "Ò",
        "\\^o": "ô", "\\^O": "Ô",
        "\\\"o": "ö", "\\\"O": "Ö",
        "\\\'u": "ú", "\\\'U": "Ú",
        "\\`u": "ù", "\\`U": "Ù",
        "\\^u": "û", "\\^U": "Û",
        "\\\"u": "ü", "\\\"U": "Ü",
        "\\c c": "ç", "\\c C": "Ç",
        
        # Others
        "{\\o}": "ø", "{\\O}": "Ø",
        "{\\aa}": "å", "{\\AA}": "Å",
        "{\\ae}": "æ", "{\\AE}": "Æ",
        "\\o": "ø", "\\O": "Ø",
        "\\aa": "å", "\\AA": "Å",
        "\\ae": "æ", "\\AE": "Æ",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def bibtex_to_markdown(bibtex_file, output_dir):
    """Convert BibTeX entries to Hugo markdown files."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse BibTeX file
    with open(bibtex_file, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    
    for entry in bib_database.entries:
        # Pre-process all text fields to replace special characters
        for key, value in entry.items():
            if isinstance(value, str):
                entry[key] = replace_special_characters(value)
        
        # Generate filename from ID
        filename = entry['ID'] + '.md'
        filepath = os.path.join(output_dir, filename)
        
        # Extract fields
        title = entry.get('title', '').strip('{}')
        year = entry.get('year', '')
        date = format_date(year)
        authors = format_authors(entry.get('author', ''))
        journal = entry.get('journal', entry.get('booktitle', ''))
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '').replace('--', '-')
        doi = entry.get('doi', '')
        citation = format_citation(entry)
        
        # Format the bibtex entry with consistent structure
        bibtex_str = format_bibtex(entry)
        
        # Replace ampersands with "and" in authors and citation (but not in bibtex)
        authors = authors.replace(' \&', ' and ')
        citation = citation.replace(' & ', ' and ')
        
        # Create markdown content
        markdown_content = f"""---
title: "{title}"
date: {date}
draft: false
authors: "{authors}"
journal: "{journal}"
volume: "{volume}"
issue: "{number}"
pages: "{pages}"
doi: "{doi}"
abstract: ""
tags: []
categories: []
featured: false
pdf: ""
code: ""
slides: ""
poster: ""
citation: "{citation}"
bibtex: >-
{bibtex_str}
references: >-

---

## Introduction

## Methods

## Results

## Discussion

## Conclusions

## Acknowledgments
"""     
        
        
        markdown_content = markdown_content.replace('\&','&')
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as mdfile:
            mdfile.write(markdown_content)
        
        print(f"Created: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert BibTeX entries to Hugo markdown files.')
    parser.add_argument('bibtex_file', help='Path to the BibTeX file')
    parser.add_argument('--output_dir', default='content/publications', help='Output directory for markdown files')
    args = parser.parse_args()
    
    bibtex_to_markdown(args.bibtex_file, args.output_dir)
    print("Conversion complete!")