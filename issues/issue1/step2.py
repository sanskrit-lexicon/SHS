import os
import re

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # (1) If there are multiple tabs '\t+', change them to one tab.
    content = re.sub(r'\t+', '\t', content)

    # (2) Convert tab to newline.
    content = content.replace('\t', '\n')

    # (2.5) '∙²' to '.²'
    content = content.replace('∙²', '.²')

    # (3) Remove blank lines.
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']

    final_text = '\n'.join(non_empty_lines)
    
    # Remove leading spaces
    final_text = re.sub(r'(?m)^[ ]+', '', final_text)

    # Swap punctuation out of closing tags (specifically handling periods, commas, or danda '।' which maps to period '.')
    final_text = re.sub(r'([,.])%\}', r'%}\1', final_text)
    final_text = re.sub(r'([,.])#\}', r'#}\1', final_text)
    final_text = re.sub(r'।%\}', r'%}.', final_text)
    final_text = re.sub(r'।#\}', r'#}.', final_text)

    # Convert '.).' to ').'
    final_text = final_text.replace('.).', ').')
    final_text = final_text.replace('.)', ').')

    with open(output_path, 'w', encoding='utf-8') as f:


        f.write(final_text + '\n')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'shs-AB.txt')
    output_file = os.path.join(script_dir, 'temp_shs_2.txt')
    
    process_file(input_file, output_file)
    print(f"Processed {input_file} -> {output_file}")
