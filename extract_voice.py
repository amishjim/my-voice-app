import json
import re
import os

def process_data(json_files, output_file_path, lyrics_only=False):
    """
    Extracts voice from any Facebook JSON files and appends to the master file.
    
    Args:
        json_files (list): List of paths to JSON files
        output_file_path (str): Path to My_Voice_Master.txt
        lyrics_only (bool): If True, double space the output.
    """
    
    extracted_text = []

    # Helper function to clean and filter text
    def clean_text(text):
        if not text or not isinstance(text, str):
            return None
        
        # Remove links
        text = re.sub(r'http\S+', '', text).strip()
        
        # Remove system text
        system_phrases = ["updated their status", "added a new photo", "shared a memory", "was with", "is with", "to their timeline"]
        for phrase in system_phrases:
            if phrase.lower() in text.lower():
                return None 
        
        words = text.split()
        word_count = len(words)
        
        # Filter: > 20 words OR (> 10 words AND human markers)
        human_markers = ["I'm", "don't", "can't", "won't", "it's", "that's", "...", "My", "my", "I've", "I'll", "you're", "we're"]
        
        has_human_marker = any(marker in text for marker in human_markers)
        
        if word_count > 20:
            return text
        elif word_count > 10 and has_human_marker:
            return text
            
        return None

    # Recursive function to search for text fields
    def extract_from_object(obj, path=""):
        """Recursively search for 'post', 'comment', 'message' fields in nested structures."""
        
        # Skip if we're in media or album folders
        if any(folder in path.lower() for folder in ['media', 'album']):
            return
        
        if isinstance(obj, dict):
            # Check for text fields
            for key in ['post', 'comment', 'message']:
                if key in obj:
                    value = obj[key]
                    # Handle both string values and nested dicts
                    if isinstance(value, str):
                        cleaned = clean_text(value)
                        if cleaned:
                            extracted_text.append(cleaned)
                    elif isinstance(value, dict):
                        # Sometimes 'comment' has nested structure like {'comment': 'text'}
                        extract_from_object(value, f"{path}/{key}")
            
            # Recurse into all values
            for key, value in obj.items():
                extract_from_object(value, f"{path}/{key}")
                
        elif isinstance(obj, list):
            # Recurse into list items
            for i, item in enumerate(obj):
                extract_from_object(item, f"{path}[{i}]")

    # Process all JSON files
    for json_file_path in json_files:
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                extract_from_object(data, os.path.basename(json_file_path))
                
        except Exception as e:
            print(f"Error processing {json_file_path}: {e}")
            # Continue processing other files instead of failing completely

    # Write to Output (Append Mode)
    try:
        if extracted_text:
            with open(output_file_path, 'a', encoding='utf-8') as f:
                for line in extracted_text:
                    f.write(line + "\n")
                    if lyrics_only:
                        f.write("\n")  # Add extra newline for double spacing
            return True, f"Successfully processed {len(json_files)} file(s) and appended {len(extracted_text)} text entries."
        else:
            return True, f"Processed {len(json_files)} file(s) but found no text matching the filters."
    except Exception as e:
        return False, f"Error writing to file: {e}"
