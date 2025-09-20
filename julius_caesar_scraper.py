# Julius Caesar scraper using the exact same format as Coriolanus
# This will create a text file with the same format as Coriolanus_structured.txt

import requests
import re

def scrape_julius_caesar():
    """
    Scrapes Shakespeare's Julius Caesar from MIT website and formats it exactly like Coriolanus.
    """
    base_url = "http://shakespeare.mit.edu/julius_caesar/"
    
    try:
        # Get the main index page
        response = requests.get(base_url + "index.html")
        response.raise_for_status()
        
        # Parse HTML manually to find all scene links
        content = response.text
        
        # Create output file
        output_lines = []
        
        # Find all scene links with the correct pattern: julius_caesar.X.Y.html
        scene_links = re.findall(r'href="(julius_caesar\.\d+\.\d+\.html)"', content)
        
        print(f"Found {len(scene_links)} scene links")
        
        # Sort the links to ensure proper order
        scene_links.sort()
        
        print(f"Processing {len(scene_links)} scenes...")
        
        for i, href in enumerate(scene_links):
            # Extract act and scene numbers from href
            match = re.search(r'julius_caesar\.(\d+)\.(\d+)\.html', href)
            if not match:
                continue
            
            act_num = match.group(1)
            scene_num = match.group(2)
            
            # Get the scene page
            scene_url = base_url + href
            print(f"[{i+1}/{len(scene_links)}] Fetching ACT {act_num} SCENE {scene_num}")
            
            try:
                scene_response = requests.get(scene_url)
                scene_response.raise_for_status()
                scene_content = scene_response.text
                
                # Add scene heading - SAME FORMAT AS CORIOLANUS
                heading = f"ACT {act_num} SCENE {scene_num}"
                output_lines.append(heading)
                output_lines.append("")  # Empty line after heading
                
                # Process the scene content using the SAME parsing as Coriolanus
                lines_added = process_scene_content_same_format(scene_content, output_lines)
                print(f"  → Processed {lines_added} lines of dialogue")
                
            except Exception as e:
                print(f"  ✗ Error processing {scene_url}: {e}")
                continue
        
        # Save the text file
        print(f"\nSaving {len(output_lines)} total lines to Julius_Caesar_structured.txt...")
        with open('Julius_Caesar_structured.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        dialogue_lines = len([line for line in output_lines if line and not line.startswith('ACT') and ':' in line])
        print("✓ Successfully saved Julius_Caesar_structured.txt")
        print(f"✓ Processed {len(scene_links)} scenes with {dialogue_lines} dialogue lines")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

def process_scene_content_same_format(scene_content, output_lines):
    """
    Process the content of a single scene using the EXACT SAME parsing as Coriolanus.
    Returns the number of dialogue lines added.
    """
    lines_added = 0
    current_speaker = None
    
    # Find all speech blocks - EXACT SAME PATTERN AS CORIOLANUS
    speech_pattern = r'<A NAME=speech\d+><b>([^<]+)</b></a>\s*<blockquote>(.*?)</blockquote>'
    speeches = re.findall(speech_pattern, scene_content, re.DOTALL)
    
    for speaker, dialogue_block in speeches:
        speaker = speaker.strip()
        
        # Extract individual dialogue lines from the blockquote - EXACT SAME PATTERN
        line_pattern = r'<A NAME=\d+>([^<]+)</A>'
        lines = re.findall(line_pattern, dialogue_block)
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Clean up the line
            line = re.sub(r'\s+', ' ', line)  # Normalize whitespace
            
            # Format the line - EXACT SAME FORMAT AS CORIOLANUS
            if speaker != current_speaker:
                current_speaker = speaker
                formatted_line = f"{lines_added + 1}: {current_speaker}: {line}"
            else:
                formatted_line = f"{lines_added + 1}: {line}"
            
            lines_added += 1
            
            # Split long lines and add to output - EXACT SAME FUNCTION
            formatted_lines = split_long_line(formatted_line)
            output_lines.extend(formatted_lines)
    
    return lines_added

def split_long_line(line, max_length=120):
    """
    Split a line if it's longer than max_length characters.
    Returns a list of lines.
    EXACT SAME FUNCTION AS CORIOLANUS
    """
    if len(line) <= max_length:
        return [line]
    
    lines = []
    current_line = ""
    words = line.split(' ')
    
    for word in words:
        if len(current_line + " " + word) <= max_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Single word longer than max_length, just add it
                lines.append(word)
    
    if current_line:
        lines.append(current_line)
    
    return lines

# Run the scraper
if __name__ == "__main__":
    scrape_julius_caesar()
