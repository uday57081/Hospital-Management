
import os
import re

d = r'c:\Users\samsung\OneDrive\文件\LOHITH PERSONAL\Hospital Management\templates'
for f in os.listdir(d):
    if f.endswith('.html'):
        path = os.path.join(d, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace filename= with path= specifically for url_for('static'
            # We look for patterns like: url_for('static', filename=
            
            # Using simple string replace might be safer if formatting is consistent, 
            # but regex handles spaces.
            
            # Pattern 1: single quotes
            new_content = re.sub(r"url_for\('static',\s*filename=", "url_for('static', path=", content)
            
            # Pattern 2: double quotes
            new_content = re.sub(r'url_for\("static",\s*filename=', 'url_for("static", path=', new_content)
             
            # Pattern 3: mixed quotes (in case) - url_for('static', filename="...")
            # The regex above handles the initial part. The value quote doesn't matter for the key replacement.

            if content != new_content:
                print(f"Fixing {f}")
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                    
        except Exception as e:
            print(f"Error processing {f}: {e}")
