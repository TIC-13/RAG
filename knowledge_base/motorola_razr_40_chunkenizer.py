"""
Separa o manual em markdown do Motorola Razr 40 (https://help.motorola.com/hc/5510/13/global/en-us/?t=index) em chunks pragmáticos, dividindo a partir da ocorrência de '#'.
"""

import argparse
import re

def Chunk(string=None, file=None, threshold=85):
    chunks = []

    def split_markdown_text(text):
        header_pattern = re.compile(r'^(#+\s)', re.MULTILINE)
        sections = header_pattern.split(text)
        combined_sections = [''.join(i) for i in zip(sections[1::2], sections[2::2])]
        if sections[0]:
            combined_sections.insert(0, sections[0])
        return combined_sections

    if string is not None:
        for i in range(len(string)):
            text_to_chunk = string[i]
            sections = split_markdown_text(text_to_chunk)
            for i in range(len(sections)):
                chunks.append(sections[i].get_content())

    if file is not None:
        for i in range(len(file)):
            with open(file[i]) as input_file:
                text_to_chunk = input_file.read()
            sections = split_markdown_text(text_to_chunk)
            for i in range(len(sections)):
                chunks.append(sections[i])

    if string is None and file is None:
        print("ERROR: You must inform one file or string for chunking.")
        return []

    return chunks

def clean_chunks(chunks):
    lines= []
    for i in range(len(chunks)):
        block = chunks[i]
        block = block.strip()
        lines.append(len(block.splitlines()))

        if '# Related topics' in block:
            block = ''
            lines[-1] = 0

        if lines[-1] < 10 and 'try these troubleshooting steps' in block:
            block = ''
            lines[-1] = 0

        if lines[-1] < 12:
            tmp = chunks[i+1]
            chunks[i+1] = block + '\n\n ' + tmp
            block = ''
            lines[-1] = 0

        chunks[i] = block

    with open("chunks.txt", "w") as file:
        for i in range(len(chunks)):
            if lines[i] > 0:
                file.write(f"<chunk>\n{chunks[i]}\n</chunk>\n\n")

    return chunks

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Chunkenizer", description="Split text into chunks")
    parser.add_argument('-t', '--threshold', metavar='VALUE', action='store', nargs=1, type=int, help='dissimilarity threshold to split chunks (default: 85)')
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to chunk')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to chunk')
    
    args = parser.parse_args()

    if args.threshold == None:
        threshold = 85
    else:
        threshold = args.threshold[0]

    chunks = Chunk(string=args.string, file=args.file, threshold=threshold)

    cleaned_chunks = clean_chunks(chunks)

    for i in range(len(cleaned_chunks)):
        print('\n<chunk>\n ' + cleaned_chunks[i] + ' \n</chunk>\n\n')
