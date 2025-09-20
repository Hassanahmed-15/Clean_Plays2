# Script to convert structured .txt files to JSON format
# Converts each .txt file to a separate JSON file with the specified format

import json
import os
import re

def convert_txt_to_json(txt_file_path):
    """
    Convert a structured .txt file to JSON format.
    Format: "ACT X, SCENE Y": { "line_number": { "play": "dialogue" } }
    """
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Create the JSON structure
        json_data = {}
        current_act_scene = None
        current_speaker = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if this is an ACT/SCENE header
            if line.startswith('ACT ') and 'SCENE ' in line:
                current_act_scene = line
                json_data[current_act_scene] = {}
                continue
            
            # Check if this is a dialogue line (format: "number: speaker: dialogue" or "number: dialogue")
            if ':' in line:
                parts = line.split(':', 2)  # Split into max 3 parts
                if len(parts) >= 2:
                    line_number = parts[0].strip()
                    
                    # Check if there's a speaker name
                    if len(parts) == 3:
                        # Format: "number: speaker: dialogue"
                        speaker = parts[1].strip()
                        dialogue = parts[2].strip()
                        current_speaker = speaker
                    else:
                        # Format: "number: dialogue" (continuation of previous speaker)
                        dialogue = parts[1].strip()
                    
                    # Only add if we have a current act/scene
                    if current_act_scene:
                        # Create the play text with speaker if available
                        if current_speaker:
                            play_text = f"{current_speaker}: {dialogue}"
                        else:
                            play_text = dialogue
                        
                        json_data[current_act_scene][line_number] = {
                            "play": play_text
                        }
        
        return json_data
    
    except Exception as e:
        print(f"Error processing {txt_file_path}: {e}")
        return None

def main():
    """
    Convert all structured .txt files to JSON format.
    """
    # Get all .txt files that end with "structured.txt"
    txt_files = [f for f in os.listdir('.') if f.endswith('_structured.txt')]
    
    print(f"Found {len(txt_files)} structured .txt files to convert:")
    for file in txt_files:
        print(f"  - {file}")
    
    converted_count = 0
    
    for txt_file in txt_files:
        print(f"\nConverting {txt_file}...")
        
        # Convert to JSON
        json_data = convert_txt_to_json(txt_file)
        
        if json_data:
            # Create JSON filename (replace .txt with .json)
            json_file = txt_file.replace('_structured.txt', '.json')
            
            # Save JSON file
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Successfully converted to {json_file}")
                converted_count += 1
                
                # Show some statistics
                total_scenes = len(json_data)
                total_lines = sum(len(scene) for scene in json_data.values())
                print(f"  → {total_scenes} scenes, {total_lines} dialogue lines")
                
            except Exception as e:
                print(f"✗ Error saving {json_file}: {e}")
        else:
            print(f"✗ Failed to convert {txt_file}")
    
    print(f"\n=== CONVERSION COMPLETE ===")
    print(f"Successfully converted {converted_count} out of {len(txt_files)} files to JSON format")
    print(f"Each JSON file contains the format: 'ACT X, SCENE Y': {{ 'line_number': {{ 'play': 'dialogue' }} }}")

if __name__ == "__main__":
    main()
