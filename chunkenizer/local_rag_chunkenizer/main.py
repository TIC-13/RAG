from autollm.utils.document_reading import read_files_as_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_index.schema import Document
from llama_index.core.callbacks import global_handlers
global_handlers.set_global_handler("simple")
import re
import warnings
import pandas as pd
import os

warnings.filterwarnings("ignore")

def chunkenize_recursive(
		input_dir, output_dir, chunk_size, 
		overlap_size, regex_removers
	):
	required_exts = [".pdf", ".md"]
	documents = read_files_as_documents(
		input_dir=input_dir,
		required_exts=required_exts
	)
	
	assert len(documents) > 0, f"No documents found in '{input_dir}'."
	
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=chunk_size,
		chunk_overlap=overlap_size,
		length_function=len,
		is_separator_regex=False,
	)
	
	for document in documents:
		text = document.text
		for regex_remover in regex_removers:
			text = re.sub(regex_remover, "", text)
		chunks = text_splitter.split_text(text)
		filename = re.sub(
        	".[A-Za-z]+_part_[0-9]+", 
         	"", 
          	os.path.basename(document.doc_id)
        ) + ".csv"
		save_to_csv(chunks, output_dir, filename)


def chunkenize_markdown_sep(
    	input_dir, output_dir
	):
	required_exts = [".md"]
	documents = read_files_as_documents(
		input_dir=input_dir,
		required_exts=required_exts
	)
	
	assert len(documents) > 0, f"No markdown documents found in '{input_dir}'."
	
	for document in documents:
		chunks = [
      		"# " + i for i in re.split("[#]+ ", document.text) if not(i.isspace())
        ][1:]
		filename = re.sub(
        	".[A-Za-z]+_part_[0-9]+", 
         	"", 
          	os.path.basename(document.doc_id)
        ) + ".csv"
		save_to_csv(chunks, output_dir, filename)
  
  
def chunkenize_semantic(
    	input_dir, output_dir, buffer_size, threshold
	):
	raise NotImplementedError("semantic chunking is not available")
		

def save_to_csv(chunks, output_dir, filename):
	pd.Series(
		chunks, name="chunks"
	).map(
		lambda x: x.replace("\n", "\\n").replace("\t", "").replace("|", "</vbar>")
	).to_csv(
		os.path.join(output_dir, filename), index=False, sep="|"
	)
	
