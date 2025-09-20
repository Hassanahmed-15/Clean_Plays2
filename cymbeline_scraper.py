# Cymbeline scraper with different text format
# This creates a more theatrical format with stage directions and enhanced formatting

import requests
import re

def scrape_cymbeline():
    """
    Scrapes Shakespeare's Cymbeline from MIT website and formats it in a theatrical style.
    """
    base_url = "http://shakespeare.mit.edu/cymbeline/"
    
    try:
        # Get the main index page
        response = requests.get(base_url + "index.html")
        response.raise_for_status()
        
        # Parse HTML manually to find all scene links
        content = response.text
        
        # Create output file
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("CYMBELINE")
        output_lines.append("by William Shakespeare")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        # Find all scene links with the correct pattern: cymbeline.X.Y.html
        scene_links = re.findall(r'href="(cymbeline\.\d+\.\d+\.html)"', content)
        
        print(f"Found {len(scene_links)} scene links")
        
        # Sort the links to ensure proper order
        scene_links.sort()
        
        print(f"Processing {len(scene_links)} scenes...")
        
        for i, href in enumerate(scene_links):
            # Extract act and scene numbers from href
            match = re.search(r'cymbeline\.(\d+)\.(\d+)\.html', href)
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
                
                # Add scene heading with enhanced formatting
                output_lines.append("")
                output_lines.append("-" * 60)
                output_lines.append(f"ACT {act_num}, SCENE {scene_num}")
                
                # Extract and add scene location
                location = extract_scene_location(scene_content)
                if location:
                    output_lines.append(f"Location: {location}")
                
                output_lines.append("-" * 60)
                output_lines.append("")
                
                # Process the scene content using theatrical format
                lines_added = process_scene_content_theatrical(scene_content, output_lines)
                print(f"  → Processed {lines_added} lines of dialogue")
                
            except Exception as e:
                print(f"  ✗ Error processing {scene_url}: {e}")
                continue
        
        # Save the text file
        print(f"\nSaving {len(output_lines)} total lines to Cymbeline_theatrical.txt...")
        with open('Cymbeline_theatrical.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        
        dialogue_lines = len([line for line in output_lines if line and 'SPEAKER:' in line])
        print("✓ Successfully saved Cymbeline_theatrical.txt")
        print(f"✓ Processed {len(scene_links)} scenes with {dialogue_lines} dialogue lines")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

def extract_scene_location(scene_content):
    """
    Extract the scene location from the HTML title or content.
    """
    # Look for title pattern: "SCENE X. Location description"
    title_match = re.search(r'<title>SCENE [IVX]+\.\s*([^<]+)</title>', scene_content, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    
    # Look for h3 heading pattern
    h3_match = re.search(r'<h3>SCENE [IVX]+\.\s*([^<]+)</h3>', scene_content, re.IGNORECASE)
    if h3_match:
        return h3_match.group(1).strip()
    
    return None

def process_scene_content_theatrical(scene_content, output_lines):
    """
    Process the content of a single scene using theatrical formatting.
    Returns the number of dialogue lines added.
    """
    lines_added = 0
    current_speaker = None
    
    # Extract stage directions first
    stage_directions = extract_stage_directions(scene_content)
    for direction in stage_directions:
        output_lines.append(f"[STAGE DIRECTION: {direction}]")
        output_lines.append("")
    
    # Find all speech blocks
    speech_pattern = r'<A NAME=speech\d+><b>([^<]+)</b></a>\s*<blockquote>(.*?)</blockquote>'
    speeches = re.findall(speech_pattern, scene_content, re.DOTALL)
    
    for speaker, dialogue_block in speeches:
        speaker = speaker.strip()
        
        # Extract individual dialogue lines from the blockquote
        line_pattern = r'<A NAME=\d+>([^<]+)</A>'
        lines = re.findall(line_pattern, dialogue_block)
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Clean up the line
            line = re.sub(r'\s+', ' ', line)  # Normalize whitespace
            
            # Format the line in theatrical style
            if speaker != current_speaker:
                current_speaker = speaker
                # Add speaker name with enhanced formatting
                output_lines.append("")
                output_lines.append(f"SPEAKER: {current_speaker.upper()}")
                output_lines.append(f"DIALOGUE: {line}")
            else:
                # Continue with same speaker
                output_lines.append(f"CONTINUED: {line}")
            
            lines_added += 1
    
    return lines_added

def extract_stage_directions(scene_content):
    """
    Extract stage directions from the scene content.
    """
    stage_directions = []
    
    # Look for italic stage directions in blockquotes
    direction_pattern = r'<blockquote>\s*<i>([^<]+)</i>\s*</blockquote>'
    directions = re.findall(direction_pattern, scene_content, re.IGNORECASE)
    
    for direction in directions:
        direction = re.sub(r'\s+', ' ', direction).strip()
        if direction:
            stage_directions.append(direction)
    
    return stage_directions

# Run the scraper
if __name__ == "__main__":
    scrape_cymbeline()
