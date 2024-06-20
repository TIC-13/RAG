import argparse
from mediapipe.tasks import python
from mediapipe.tasks.python import text
import time

def Embed(model, string=None, file=None):

    model_path = model[0]
    embeddings = []

    # print('\n', model, string, file, '\n')

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = text.TextEmbedderOptions(base_options=base_options)

    with text.TextEmbedder.create_from_options(options) as embedder:
        if string is not None:
            start_embed_time = time.time()
            for i in range(len(string)):
                text_to_embed = string[i]
                embedding_result = embedder.embed(text_to_embed)
                # print(embedding_result.embeddings[0])
                embeddings.append(
                    { 'embed': embedding_result.embeddings[0],
                      'sentence': text_to_embed }
                    )
            
            end_embed_time = time.time()
            exec_embed_time = end_embed_time - start_embed_time
            print("\nExecution time in ms:",exec_embed_time*1000,"\nExecution time in ms per embedding:",(exec_embed_time*1000)/len(args.string)) 

        if file is not None:
            start_read_time = time.time()
            for i in range(len(file)):
                with open(file[i]) as input_file:
                    text_to_embed = input_file.read().split("\n")

                # for j in range(len(file_paragraphs)):
                #     chunks_to_embed = chunk(text_to_embed)
                
                start_embed_time = time.time()
                for j in range(len(text_to_embed)):
                    embedding_result = embedder.embed(text_to_embed[j])
                    # print(embedding_result.embeddings[0])
                    embeddings.append(
                    { 'embed': embedding_result.embeddings[0],
                      'sentence': text_to_embed[j] }
                    )
                
                end_embed_time = time.time()
                exec_embed_time = end_embed_time - start_embed_time
                print("\nExecution time of file",i+1,"in ms:",exec_embed_time*1000,"\nExecution time in ms per embedding:",(exec_embed_time*1000)/len(text_to_embed)) 

            end_read_time = time.time()
            exec_read_time = end_read_time - start_read_time
            print("Total execution time in ms:",exec_read_time*1000,'\n') 

        if string is None and file is None:
            raise Exception("You must inform at least one file or string to embed.")
        
        return embeddings

                
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Embedder", usage="Pass a text embedding model and text file(s) or string(s) to embed", description="Runs a model to embed text")
    parser.add_argument('-m', '--model', action='store', nargs=1, type=str, help='PATH of the embedding model')
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to embed')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to embed')
    args = parser.parse_args()

    embeddings = Embed(model=args.model, string=args.string, file=args.file)
    for obj in embeddings:
        print('embed:',obj['embed'],'\nsentence:',obj['sentence'],'\n')