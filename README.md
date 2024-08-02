# Retrieval Augmented Generation (RAG)
Pipeline to execute RAG on Desktop and Mobile with high performance

---

This repository not only contains the rag execution pipeline, but also the preparation files for executing the pipeline, for example, programs for building the vector store (chunkenization, pdf reading, embedding, etc).


## Setup 

On Linux:
- Clone this repo and run `git submodule update --init --recursive`
- Install [miniconda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)
- Create environment using `conda env -f environment.yml` and activate it with `conda activate local_rag`
- Install [Android Studio](https://developer.android.com/studio) and, inside the SDK Manager, go to "SDK Tools" tab and select NDK, cmake, command-line tools and platform tools
    * Set ANDROID_NDK variable so that `$ANDROID_NDK/build/cmake/android.toolchain.cmake` is available. (e.g.: `$HOME/Android/Sdk/ndk/27.0.11718014`)
    * Set TVM_NDK_CC variable to clang compiler. (e.g.: `$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android24-clang`)
- Install [Rust](https://www.rust-lang.org/tools/install) and make sure `rustc`, `cargo`, and `rustup` are available on the terminal
- Install JDK and set `JAVA_HOME` so `$JAVA_HOME/bin/java` is available. The version that comes bundled with Android Studio may be used (and MLC's authors recommend it)
- Set TVM_SOURCE_DIR=/path/to/mlc-llm/3rdparty/tvm (preferably the full path, not relative)
- Install mlc_llm and mlc_ai from the wheels in the Drive folder.
- Run `source $HOME/.cargo/env`
- Make sure you have Cmake and git-lfs installed. Conda can be used for this: `conda install -c conda-forge cmake ninja git git-lfs`
- Persisting the environment values is recommended
- If a model needs to be added or removed, modify `MLCChat/mlc-package-config.json` accordingly, before continuing
- On terminal:
    * `cd /path/to/MLCChat`
    * `export MLC_LLM_SOURCE_DIR=/path/to/mlc-llm` (avoid relative path)
    * `mlc_llm package` (`MLC_JIT_POLICY=REDO mlc_llm package` if you need to force rebuild)
- Back at the root of the repo, run `make all_android`
- Open `mlc/android/MLCChat` inside Android Studio to generate the apk
- Enjoy a fully local RAG application
