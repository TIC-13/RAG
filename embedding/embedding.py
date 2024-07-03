import argparse
from mediapipe.tasks import python
from mediapipe.tasks.python import text
from chunkenizer.chunkenizer import Chunk

def Embed(model, string=None, file=None):

    model_path = model[0]
    embeddings = []

    # print('\n', model, string, file, '\n')

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = text.TextEmbedderOptions(base_options=base_options)

    with text.TextEmbedder.create_from_options(options) as embedder:
        if string is not None:
            for i in range(len(string)):
                text_to_embed = string[i]
                embedding_result = embedder.embed(text_to_embed)
                # print(embedding_result.embeddings[0])
                embeddings.append(
                    { 'embed': embedding_result.embeddings[0],
                      'sentence': text_to_embed }
                    )
                

        if file is not None:
            chunks_to_embed = Chunk(file=file)

            for i in range(len(chunks_to_embed)):
                embedding_result = embedder.embed(chunks_to_embed[i])
                # print(embedding_result.embeddings[0])
                embeddings.append(
                {   'embed': embedding_result.embeddings[0],
                    'sentence': chunks_to_embed[i] }
                )

        if string is None and file is None:
            print("ERROR: You must inform at least one file or string to embed.")
            return []
        
        f = open("embedding.csv", "w+")
        for obj in embeddings:
            f.write(str(obj['embed'].embedding[0]))
            f.write("\n")
            for i in range(len(obj['embed'].embedding)-1):
                f.write(" " + str(obj['embed'].embedding[i+1]))

        f = open("chunks.csv", "w+")
        f.write(embeddings[0]['sentence'])
        for i in range(len(embeddings)-1):
            f.write("\n>>>>>>>>>>>>>>@<<<<<<<<<<<<<<\n")
            f.write(embeddings[i+1]['sentence'])

                
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Embedder", usage="Pass a text embedding model and text file(s) or string(s) to embed", description="Runs a model to embed text")
    parser.add_argument('-m', '--model', action='store', nargs=1, type=str, help='PATH of the embedding model')
    parser.add_argument('-s', '--string', action='store', nargs='+', type=str, help='string(s) to embed')
    parser.add_argument('-f', '--file', action='store', nargs='+', type=str, help='PATH of file(s) to embed')
    args = parser.parse_args()

    embeddings = Embed(model=args.model, string=args.string, file=args.file)
    for obj in embeddings:
        print("embed:",obj['embed'].embedding,"\n\n")
        # print('embed:',obj['embed'],'\nsentence:',obj['sentence'],'\n')