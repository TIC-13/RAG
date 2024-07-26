import click
import yaml

from local_rag_embedder import main

@click.group()
def cli():
    """
    CLI for local_rag_embedder
    """
    pass


@cli.command()
@click.option(
    "-c",
    "--chunks_directory",
    help=(
        "Path to directory contain chunkenized documents as csv files. " \
        + "All of them must be in the same directory."
    )
)
@click.option(
    "-o", 
    "--output_path",
    help=(
        "Path to output directory."
    )
)
@click.option(
	"-m",
    "--model",
    type=click.Choice(
        [
            "universal_sentence_encoder",
        ]
    ),
    help=(
    	"Embedding model."
    )
)
def generate_embeddings(
		chunks_directory, output_path, model
	):
    """
    Entry point to start embedding.
    """
    main.embed_chunks(
        chunks_directory, output_path, model
    )
