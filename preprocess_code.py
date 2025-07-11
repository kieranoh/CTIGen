import os
import re
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
SAMPLE_HASH = os.getenv("SAMPLE_HASH")
GHIDRA_OUTPUT_DIR = os.getenv("GHIDRA_OUTPUT_DIR")
PREPROCESS_OUTPUT_DIR = os.getenv("PREPROCESS_OUTPUT_DIR")

input_file_path = os.path.join(GHIDRA_OUTPUT_DIR, f"{SAMPLE_HASH}_exe.txt")
os.makedirs(PREPROCESS_OUTPUT_DIR, exist_ok=True)
cleaned_file_path = os.path.join(PREPROCESS_OUTPUT_DIR, f"{SAMPLE_HASH}.txt")
json_output_path = os.path.join(PREPROCESS_OUTPUT_DIR, f"{SAMPLE_HASH}.json")

with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

content = re.sub(r'/\*.*?WARNING.*?\*/', '', content, flags=re.DOTALL)
content = re.sub(r'Parameter:.*\n', '', content)
content = re.sub(r'Called by:.*\n', '', content)

with open(cleaned_file_path, 'w', encoding='utf-8') as file:
    file.write(content)
print(f"Preprocessing complete. File saved to: {cleaned_file_path}")

function_names, addresses, source_codes = [], [], []

with open(cleaned_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

current_function_name = None
current_address = None
current_source_code = []
capturing_code = False

for line in lines:
    if "Function Found:" in line:
        if current_function_name:
            source_codes.append("\n".join(current_source_code).strip())
            current_source_code = []

        current_function_name = line.split(":", 1)[1].strip()
        function_names.append(current_function_name)

    elif "Address:" in line:
        current_address = line.split(":", 1)[1].strip()
        addresses.append(current_address)

    elif "Decompiled C Code:" in line:
        capturing_code = True

    elif capturing_code:
        current_source_code.append(line.strip())

if current_function_name:
    source_codes.append("\n".join(current_source_code).strip())

df = pd.DataFrame({
    "Function Name": function_names,
    "Address": addresses,
    "Source Code": source_codes
})
df.to_json(json_output_path, orient="records", lines=True, force_ascii=False)

print(f"Extracted function data saved to JSON: {json_output_path}")