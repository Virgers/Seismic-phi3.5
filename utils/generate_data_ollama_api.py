import requests
import json
import time

# Replace with your actual LLaMA API endpoint
API_ENDPOINT = "http://localhost:11434/api/generate" 

def generate_response(prompt):
    
    data = {
        "model": "mistral-nemo:latest",  # Adjust if needed
        "format": "json",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(API_ENDPOINT, json=data)
    response_dict = json.loads(response.text)
    response_content = response_dict["response"]
    
    return response_content

# Load instructions from the JSON file
instructions_json = '/home/dell/disk1/Jinlong/Seismic-phi3/dataset/data/instructions.json'

with open(instructions_json, "r") as f:
    instruction_data = json.load(f)

results = []  

# Generate responses for each instruction
for instruction in instruction_data:
    prompt = instruction.get("instruction", "")  # Get the text of each instruction
    if prompt:  # Ensure there's a prompt to send
        response = generate_response(prompt)
        
        time.sleep(2) 

        if response:
            # Remove newline characters from the response
            cleaned_response = response.replace("\n", " ")
            results.append({
                "instruction": prompt,  # Use "question" for clarity
                "input": "",
                "output": cleaned_response   
            })

# Save the results to a new JSON file
with open("generated_dataset.json", "w") as f:
    json.dump(results, f, indent=4)

print("Generated dataset saved to 'generated_dataset.json'.")
