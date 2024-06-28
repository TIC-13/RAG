#!/bin/bash

#httrack https://help.motorola.com/hc/5510/13/global/en-us/index.html -O ./razr_40

input_dir="./razr_40/help.motorola.com/hc/5510/13/global/en-us"


output_dir="./razr_40/help.motorola.com/hc/5510/13/global/en-us/txts"
mkdir -p $output_dir
for html_file in "$input_dir"/*.html; do
  base_name=$(basename "$html_file" .html)
  html2text "$html_file" > "$output_dir/$base_name.txt"
done

echo "Conversão concluída. Os arquivos TXT estão em $output_dir"

echo "" > ./razr_40/complete_manual.txt

cd razr_40/help.motorola.com/hc/5510/13/global/en-us/txts/

cat *.txt >> ../../../../../../../complete_manual.txt

cd ../../../../../../../

cat << 'EOF' > remove_text.py
import os
import re

input_file_path = "./complete_manual.txt"

feedback_text_to_remove = """Was this information helpful?

YesNo

Thanks for letting us know

What question are you trying to answer?

Glad it helped

Share more feedback here

Glad it helped

Do not share any personal info

Thanks for your feedback!"""

png_link_to_remove = "![](https://help.motorola.com/hc/images/global/"
png_extension_to_remove = ".png)"

with open(input_file_path, 'r') as file:
    file_content = file.read()

file_content = file_content.replace(feedback_text_to_remove, "")
file_content = file_content.replace(png_link_to_remove, "image:")
file_content = file_content.replace(png_extension_to_remove, "")

pattern = re.compile(r'\[([^\]]*?)\]\([^)]*\)', re.DOTALL)
def replace_text(match):
    replacement = match.group(1).replace('\n', ' ')
    return replacement
file_content = re.sub(pattern, replace_text, file_content)


with open(input_file_path, 'w') as file:
    file.write(file_content)

print(f"Texto removido com sucesso do arquivo {input_file_path}")
EOF

python3 remove_text.py
