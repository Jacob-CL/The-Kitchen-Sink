import argparse
import os
import re

def load_patterns(pattern_file='CTFpatterns.txt'):
    """Load search patterns from the specified file."""
    try:
        with open(pattern_file, 'r', encoding='utf-8') as file:
            patterns = [line.strip() for line in file if line.strip()]
        return patterns
    except FileNotFoundError:
        print(f"Pattern file '{pattern_file}' not found.")
        exit(1)

def grep_files(directory, patterns):
    """Recursively search for patterns in files under the given directory."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file, 1):
                        for pattern in patterns:
                            if re.search(pattern, line):
                                print(f"Match found in {file_path} on line {line_num}: {line.strip()}")
            except UnicodeDecodeError:
                # Skipping binary or non-text files
                continue
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")