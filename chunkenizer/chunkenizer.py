from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import argparse
import pandas as pd


def SemanticSplit(buffer_size, threshold, text_to_chunk):
    embedder = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    splitter = SemanticSplitterNodeParser(
        buffer_size=buffer_size, breakpoint_percentile_threshold=threshold, embed_model=embedder
    )
    document = [Document(text=text_to_chunk)]
    nodes = splitter.get_nodes_from_documents(document)
    return nodes


def MarkdownSplit(text_to_chunk):
    nodes = ["#"+str for str in text_to_chunk.split("#")]
    nodes.pop(0)
    return nodes


def Chunk(string=None, file=None, chunking='markdown', threshold=85, buffer_size=1): 
    if string is None and file is None:
        print("ERROR: You must inform one file or string for chunking.")
        return []
    
    # print(string,file,chunking,threshold,buffer_size)
    chunks = []

    if string is not None:
        text_to_chunk = string[i]

        if chunking == 'markdown':
            nodes = MarkdownSplit(text_to_chunk)
            for j in range(len(nodes)):
                chunks.append(nodes[j])
        elif chunking == 'semantic':
            nodes = SemanticSplit(buffer_size, threshold, text_to_chunk)
            for j in range(len(nodes)):
                chunks.append(nodes[j].get_content())

    if file is not None:
        for i in range(len(file)):
            with open(file[i]) as input_file:
                text_to_chunk = input_file.read()

            if chunking == 'markdown':
                nodes = MarkdownSplit(text_to_chunk)
                for j in range(len(nodes)):
                    chunks.append(nodes[j])
            elif chunking == 'semantic':
                nodes = SemanticSplit(buffer_size, threshold, text_to_chunk)
                for j in range(len(nodes)):
                    chunks.append(nodes[j].get_content())

            # print(nodes)

        # print(chunks)

    pd.Series(chunks, name="chunks").map(lambda str: str.replace("\n","\\n").replace("\t","")).to_csv("chunks.csv", index=False, sep="%")
    return chunks


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Chunkenizer", description="Split text into chunks")
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to chunk')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to chunk')
    parser.add_argument('--split', action='store', nargs=1, type=str, help='chunking strategy: markdown, semantic (default: markdown)')
    parser.add_argument('-t', '--threshold', metavar='VALUE', action='store', nargs=1, type=int, help='dissimilarity threshold to split chunks - semantic only (default: 85)')
    parser.add_argument('-a', '--append', metavar='SIZE', action='store', nargs=1, type=int, help='setences grouped for similarity evaluation - semantic only (default: 1)')
    parser.set_defaults(threshold=85)
    parser.set_defaults(split=['markdown'])
    parser.set_defaults(append=1)
    args = parser.parse_args()

    # print(args)
    chunks = Chunk(string=args.string, file=args.file, chunking=args.split[0], threshold=args.threshold, buffer_size=args.append)
    # print('chunks:', len(chunks),'\n')
    # print(chunks[0])
    # for i in range(len(chunks)-1):
    #     print('>>>>>>>>>>>>>>@<<<<<<<<<<<<<<')
    #     print(chunks[i+1])