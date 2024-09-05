from mediapipe.tasks import python
from mediapipe.tasks.python import text
import tqdm
import warnings
import pandas as pd
import os
import glob
import requests
import numpy as np

warnings.filterwarnings("ignore")


MODELS_URL = {
	"universal_sentence_encoder": "https://storage.googleapis.com/mediapipe-models/text_embedder/universal_sentence_encoder/float32/latest/universal_sentence_encoder.tflite",
	"bert_embedder": "https://storage.googleapis.com/mediapipe-models/text_embedder/bert_embedder/float32/1/bert_embedder.tflite",
	"average_word_embedder": "https://storage.googleapis.com/mediapipe-models/text_embedder/average_word_embedder/float32/1/average_word_embedder.tflite"
}


def embed_chunks(
		input_dir, output_dir, model
	):
	get_embedding = lambda embedder, x: embedder.embed(x).embeddings[0].embedding
	chunk_stores = glob.glob(os.path.join(input_dir, "*.csv"))
	chunk_stores = [i for i in chunk_stores if not(os.path.basename(i).startswith("vectors_"))]
	models_directory = os.path.join(os.getcwd(), "embedding_models")
	if not(os.path.isdir(models_directory)):
		os.mkdir(models_directory)
	model_path = os.path.join(models_directory, model + ".tflite")
	if not(os.path.isfile(model_path)):
		print("Downloading model...")
		response = requests.get(MODELS_URL[model], stream=True)
		assert response.ok, f"Cannot download model. HTTP Code: {response.status_code}"
		with open(model_path, mode="wb") as file:
			for file_chunk in tqdm.tqdm(response.iter_content(chunk_size=10 * 1024), unit=' file_chunks'):
				file.write(file_chunk)
	base_options = python.BaseOptions(model_asset_path=model_path)
	options = text.TextEmbedderOptions(base_options=base_options, quantize=True, l2_normalize=True)
	embedder = text.TextEmbedder.create_from_options(options)
	for file in tqdm.tqdm(chunk_stores):
		output_filename = os.path.join(output_dir, "vectors_" + os.path.basename(file))
		chunks_to_embed = pd.read_csv(file, sep="|")["chunks"].to_list()
		vectors = []
		for chunk in tqdm.tqdm(chunks_to_embed):
			vectors.append(get_embedding(embedder, chunk))
		vectors = np.float32(vectors)
		pd.DataFrame(vectors).to_csv(output_filename, index=False)
	
