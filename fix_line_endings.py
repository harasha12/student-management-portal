# fix_line_endings.py

input_file = "requirements.txt"
output_file = "requirements_fixed.txt"

with open(input_file, "rb") as f:
    content = f.read()

# Replace CRLF with LF
clean_content = content.replace(b"\r\n", b"\n")

with open(output_file, "wb") as f:
    f.write(clean_content)

print("✅ Clean LF-only file written to", output_file)
