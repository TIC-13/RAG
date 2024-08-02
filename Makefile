# Compiladores
PY_DESKTOP = python3

# CC_DESKTOP = g++
# CC_ANDROID = $(NDK_ROOT)/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android29-clang++

# Flags de compilação
EMBEDDING_REQ = ./embedding/requirements.txt
CHUNKENIZER_REQ = ./chunkenizer/requirements.txt

# CFLAGS = -Wall -g
# ANDROID_CFLAGS = --target=aarch64-none-linux-android21 --sysroot=$(NDK_ROOT)/toolchains/llvm/prebuilt/linux-x86_64/sysroot -fPIE -fPIC

# DIR_VECTOR_STORE = /path/to/
# FILE_VECTOR_STORE=vector_store_file

########################################

all_desktop: embedding	# desktop exec_desktop
all_android: embedding

# OBJS_DESKTOP = main.o funcao1.o
# OBJS_ANDROID = main_android.o funcao1_android.o


# Regras para compilar os arquivos objeto
./venv:
	$(PY_DESKTOP) -m venv venv

VENV_PY = ./venv/bin/python3


chunkenizer:
	local_rag_chunkenizer chunkenize -d data/ -o data/ -m recursive
	local_rag_chunkenizer chunkenize -d data/ -o data/ -m markdown_sep

embedding: chunkenizer
	local_rag_embedder generate-embeddings -c data/ -o data/ -m universal_sentence_encoder
	cp embedding_models/universal_sentence_encoder.tflite mlc/android/MLCChat/app/src/main/assets/universal_sentence_encoder.tflite



# main.o: main.cpp
# 	$(CC_DESKTOP) $(CFLAGS) -c main.cpp -o main.o

# funcao1.o: funcao1.cpp funcao1.h
# 	$(CC_DESKTOP) $(CFLAGS) -c funcao1.cpp -o funcao1.o


# Regras para compilar os arquivos objeto para Android
# main_android.o: main.cpp
# 	$(CC_ANDROID) $(ANDROID_CFLAGS) -c main.cpp -o main_android.o

# funcao1_android.o: funcao1.cpp funcao1.h
# 	$(CC_ANDROID) $(ANDROID_CFLAGS) -c funcao1.cpp -o funcao1_android.o

# desktop: $(OBJS_DESKTOP)
# 	$(CC_DESKTOP) $(CFLAGS) -o build/reggae $(OBJS_DESKTOP)

# exec_desktop:
# 	./build/reggae $(DIR_VECTOR_STORE)/$(FILE_VECTOR_STORE)

# android: $(OBJS)
# 	$(CC_ANDROID) $(ANDROID_CFLAGS) -o build/reggae $(OBJS)

# DIR_ANDROID_WORKSPACE = /data/local/tmp/rag
# exec_android:
# 	adb shell mkdir -p $(DIR_ANDROID_WORKSPACE)
# 	adb push build/reggae $(DIR_ANDROID_WORKSPACE)
# 	adb shell chmod +x $(DIR_ANDROID_WORKSPACE)/reggae
# 	adb push $(DIR_VECTOR_STORE)/$(FILE_VECTOR_STORE) $(DIR_ANDROID_WORKSPACE)/$(FILE_VECTOR_STORE)
# 	adb shell $(DIR_ANDROID_WORKSPACE)/reggae $(DIR_ANDROID_WORKSPACE)/$(FILE_VECTOR_STORE)

clean:
	rm -rf __pycache__
	rm -rf ./venv

# 	rm -f $(OBJS_DESKTOP) $(OBJS_ANDROID) /build/reggae 

.PHONY: embedding chunkenizer common_environment