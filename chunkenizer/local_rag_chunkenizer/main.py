from autollm.utils.document_reading import read_files_as_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import warnings
import pandas as pd
import os

warnings.filterwarnings("ignore")

def chunkenize_recursive(
		input_dir, output_dir, chunk_size, 
		overlap_size, regex_removers
	):
	required_exts = [".pdf"]
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
		filename = os.path.basename(documents[0].doc_id) + ".csv"
		pd.Series(
			chunks, name="chunks"
		).map(
			lambda x: x.replace("\n", "\\n").replace("\t", "")
		).to_csv(
			os.path.join(output_dir, filename), index=False, sep="|"
		)
	
