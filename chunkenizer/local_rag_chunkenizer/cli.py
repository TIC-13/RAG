import click
import yaml

from local_rag_chunkenizer import main

@click.group()
def cli():
    """
    CLI for local_rag_chunkenizer
    """
    pass


@cli.command()
@click.option(
    "-d",
    "--documents_path",
    help=(
        "Path to documents directory. All of them must be in the same directory."
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
    "--method",
    type=click.Choice(
        [
            "recursive",
            "semantic",
        ]
    ),
    help=(
    	"Chunkenization method."
    )
)
@click.option(
	"--chunk_size",
	default=400, 
	type=click.INT,
    help=(
    	"Chunk size for recursive chunkenization."
    )
)
@click.option(
	"--overlap",
	default=40, 
	type=click.INT,
    help=(
    	"Chunk overlap size for recursive chunkenization."
    )
)
@click.option(
	"-r",
	"--regex_removers",
	default=["\\n[0-9]+"],
	multiple=True,
    help=(
    	"Removes from the text any expression that matches it. " +\
    	"Useful for ASCII codes and such."
    )
)
def chunkenize(
		documents_path, output_path, 
		method, chunk_size, overlap, regex_removers
	):
    """
    Entry point to start chunkenizing.
    """
    if method == None:
    	raise ValueError("Method can't be 'None'")
    if method == "recursive":
    	main.chunkenize_recursive(
    		documents_path, output_path, chunk_size, overlap, regex_removers
    	)
    else:
    	raise NotImplementedError("Semantic chunkenization is not available yet.")
