import os
import fitz # PyMuPDF
import json
import re
from fuzzywuzzy import process

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIND_PDF = os.path.join(BASE_DIR, "Wind Table.pdf")
SEISMIC_PDF = os.path.join(BASE_DIR, "Seismic Table.pdf")
TEMP_PDF = os.path.join(BASE_DIR, "Temperature Table.pdf")
OUTPUT_JSON = os.path.join(BASE_DIR, "data", "india_data.json")

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('\u2013', '-').strip()
    return re.sub(r'\s+', ' ', text)

def get_pdf_text(path):
    if not os.path.exists(path):
        print(f"Missing: {path}")
        return []
    doc = fitz.open(path)
    lines = []
    for page in doc:
        text = page.get_text("text") # simple text
        lines.extend([clean_text(l) for l in text.split('\n') if l.strip()])
    return lines

def parse_temp_hierarchy():
    # Attempt to build State -> City map from Temp PDF
    # Assumption based on "State-wise" title:
    # Lines might look like: "StateName" ... "CityName" ... data
    # OR Table stricture.
    # We will look for list of standard Indian states to assist parsing if headers aren't clear.
    
    lines = get_pdf_text(TEMP_PDF)
    print(f"Temp PDF Lines: {len(lines)}")
    
    data = {}
    current_state = "Unknown State"
    
    # Heuristic: States are usually purely alphabetic strings, often detached provided in sorted order
    # But text extraction might mix columns.
    # Let's try a regex for the data row first: "City Max Min"
    
    # Common States List for detection
    STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", 
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", 
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman & Nicobar", "Chandigarh", "Dadra & Nagar Haveli", "Daman & Diu", 
        "Delhi", "Lakshadweep", "Puducherry"
    ]
    
    for line in lines:
        # Check if line matches a State Name exactly or closely
        clean = line.strip()
        is_state = False
        for s in STATES:
            if s.lower() == clean.lower() or s.lower() in clean.lower(): 
                # Be careful not to match "West Bengal" in "West Bengal City" row
                # If the line is SHORT and matches state, likely a header
                if len(clean) < len(s) + 5:
                    current_state = s
                    if current_state not in data:
                        data[current_state] = {}
                    is_state = True
                    break
        if is_state: continue

        # Parse Data Row: City Max Min
        # Regex: Name (Allowing spaces) Float Float
        # Note: Sometimes extracted text splits "City" "Max" "Min" into lines. This is hard.
        # Let's assume lines are preserved or joined.
        
        # Look for pattern ending in two numbers
        match = re.search(r'([A-Za-z\s\&\(\)\.\-]+)\s+([\-]?\d{1,2}\.?\d*)\s+([\-]?\d{1,2}\.?\d*)', clean)
        if match:
             city = match.group(1).strip()
             # Cleanup city (remove leading numbers/bullets)
             city = re.sub(r'^\d+\W+', '', city)
             
             max_t = float(match.group(2))
             min_t = float(match.group(3))
             
             # Filter headers
             if max_t > 60 or max_t < -10: continue 
             
             if len(city) > 2:
                 if current_state == "Unknown State":
                     # Create a default bin if header missed
                     if "General" not in data: data["General"] = {}
                     data["General"][city] = {"max": max_t, "min": min_t}
                 else:
                     data[current_state][city] = {"max": max_t, "min": min_t}
                     
    return data

def parse_wind_flat():
    lines = get_pdf_text(WIND_PDF)
    print(f"Wind PDF Lines: {len(lines)}")
    db = {}
    for line in lines:
        # Patern: City Speed
        match = re.search(r'([A-Za-z\s\.\(\)]+)\s+(\d{2}(\.\d+)?)', line)
        if match:
            city = match.group(1).strip().upper()
            speed = float(match.group(2))
            if 30 <= speed <= 60 and len(city) > 2:
                db[city] = speed
    return db

def parse_seismic_flat():
    lines = get_pdf_text(SEISMIC_PDF)
    print(f"Seismic PDF Lines: {len(lines)}")
    db = {}
    for line in lines:
        # Pattern: City Zone (II, III, IV, V)
        match = re.search(r'([A-Za-z\s\.\(\)]+)\s+(II|III|IV|V)', line, re.IGNORECASE)
        if match:
            city = match.group(1).strip().upper()
            zone = match.group(2).upper()
            if len(city) > 2:
                db[city] = zone
    return db

def update_db_fuzzy(master, flat_data, data_key):
    # Iterate through all cities in master and try to find match in flat_data
    # flat_data keys are UPPERCASE
    
    city_list = list(flat_data.keys())
    
    for state in master:
        for city in master[state]:
            query = city.upper()
            
            # 1. Exact Match
            if query in flat_data:
                master[state][city][data_key] = flat_data[query]
                continue
                
            # 2. Fuzzy Match
            # Only if length is decent to avoid noise
            if len(query) > 3:
                match, score = process.extractOne(query, city_list)
                if score >= 90: # High confidence
                     master[state][city][data_key] = flat_data[match]
                else:
                    master[state][city][data_key] = "N/A"
            else:
                 master[state][city][data_key] = "N/A"
                 
    # Also Check for Orphaned Data (Cities in Wind/Seismic but not in Temp/Master)
    # If found, add to "General" or "Unknown"
    # For now, we prioritize the hierarchy from Temp as requested (State-wise)
    return master

def main():
    print("Building State Hierarchy from Temp Table...")
    full_db = parse_temp_hierarchy()
    
    print("Extracting Wind Data...")
    wind = parse_wind_flat()
    
    print("Extracting Seismic Data...")
    seis = parse_seismic_flat()
    
    print("Merging Data...")
    update_db_fuzzy(full_db, wind, "wind")
    update_db_fuzzy(full_db, seis, "zone")
    
    # Calculate stats
    total_cities = sum(len(v) for v in full_db.values())
    print(f"DB Built: {len(full_db)} States, {total_cities} Cities.")
    
    # Ensure directory
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(full_db, f, indent=4)
    print(f"Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
