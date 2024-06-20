from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import argparse


def Chunk(string=None, file=None, threshold=85):
    embedder = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    splitter = SemanticSplitterNodeParser(
        buffer_size=1, breakpoint_percentile_threshold=threshold, embed_model=embedder
    )
    chunks = []

    if string is not None:
        for i in range(len(string)):        
            text_to_chunk = string[i]
            document = [Document(text=text_to_chunk)]
            nodes = splitter.get_nodes_from_documents(document)
            # print(docs)
            for i in range(len(nodes)):
                chunks.append(nodes[i].get_content())
        

    if file is not None:
        for i in range(len(file)):
            with open(file[i]) as input_file:
                text_to_chunk = input_file.read()
            document = [Document(text=text_to_chunk)]

            # for j in range(len(file_paragraphs)):
            #     chunks_to_embed = chunk(text_to_embed)
            
            nodes = splitter.get_nodes_from_documents(document)
            # print(docs)
            for i in range(len(nodes)):
                chunks.append(nodes[i].get_content())
        

    if string is None and file is None:
        raise Exception("You must inform one file or string to chunk.")

    return chunks


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Chunkenizer", description="Split text into chunks")
    parser.add_argument('-t', '--threshold', metavar='VALUE', action='store', nargs=1, type=int, help='dissimilarity threshold to split chunks (default: 85)')
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to chunk')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to chunk')
    args = parser.parse_args()

    chunks = Chunk(string=args.string, file=args.file, threshold=args.threshold[0])
    print('chunks:', len(chunks),'\n')
    for i in range(len(chunks)):
        print('\n<chunk>\n',chunks[i],'\n</chunk>\n')