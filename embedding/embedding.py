import argparse
from mediapipe.tasks import python
from mediapipe.tasks.python import text
from chunkenizer.chunkenizer import Chunk
import pandas as pd

def Embed(model, string=None, file=None):

    if model is None:
        print("ERROR: You must inform the embedding model for the task.")
        return

    if string is None and file is None:
        print("ERROR: You must inform at least one file or string to embed.")
        return

    model_path = model[0]
    embeddings = []

    # print('\n', model, string, file, '\n')

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = text.TextEmbedderOptions(base_options=base_options)

    with text.TextEmbedder.create_from_options(options) as embedder:
        if string is not None:
            # start_embed_time = time.time()
            for i in range(len(string)):
                text_to_embed = string[i]
                embedding_result = embedder.embed(text_to_embed).embeddings[0].embedding
                # print(embedding_result.embeddings[0])
                embeddings.append(embedding_result)
            
            # end_embed_time = time.time()
            # exec_embed_time = end_embed_time - start_embed_time
            # print("\nExecution time in ms:",exec_embed_time*1000,"\nExecution time in ms per embedding:",(exec_embed_time*1000)/len(args.string)) 

        if file is not None:
            # start_read_time = time.time()
            chunks_to_embed = Chunk(file=file)
            
            # print("\nchunks amount:",len(chunks_to_embed),'\n')
            # start_embed_time = time.time()
            for i in range(len(chunks_to_embed)):
                embedding_result = embedder.embed(chunks_to_embed[i]).embeddings[0].embedding
                # print(embedding_result.embeddings[0])
                embeddings.append(embedding_result)
            
            # end_embed_time = time.time()
            # exec_embed_time = end_embed_time - start_embed_time
            # print("\nExecution time of file",i+1,"in ms:",exec_embed_time*1000,"\nExecution time in ms per embedding:",(exec_embed_time*1000)/len(chunks_to_embed)) 

            # end_read_time = time.time()
            # exec_read_time = end_read_time - start_read_time
            # print("Total execution time in ms:",exec_read_time*1000,'\n') 
        
        # print("\nembeddings amount:",len(embeddings),'\n')

        pd.DataFrame(embeddings).to_csv("embeddings.csv", index=False, sep="\t")

                
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Embedder", usage="Pass a text embedding model and text file(s) or string(s) to embed", description="Runs a model to embed text")
    parser.add_argument('-m', '--model', action='store', nargs=1, type=str, help='PATH of the embedding model')
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to embed')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to embed')
    args = parser.parse_args()

    Embed(model=args.model, string=args.string, file=args.file)
    # f = open("embeddings.txt")
    # print(f.read())