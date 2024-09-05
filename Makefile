########################################

all_desktop: embedding
all_android: embedding


chunkenizer:
	local_rag_chunkenizer chunkenize -d data/ -o data/ -m recursive --chunk_size 300 --overlap 40
	local_rag_chunkenizer chunkenize -d data/ -o data/ -m markdown_sep

embedding: chunkenizer
	local_rag_embedder generate-embeddings -c data/ -o data/ -m universal_sentence_encoder
	cp embedding_models/universal_sentence_encoder.tflite mlc/android/MLCChat/app/src/main/assets/universal_sentence_encoder.tflite
	cp data/*.csv mlc/android/MLCChat/app/src/main/assets/

clean:
	rm -rf data/*.csv embedding_models mlc/android/MLCChat/app/src/main/assets/*

.PHONY: embedding chunkenizer common_environment
