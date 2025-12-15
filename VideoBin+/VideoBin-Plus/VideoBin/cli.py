import click
from .encoder import encode_file
from .decoder import decode_video

@click.group()
def cli():
    pass

@cli.command()
@click.argument("input_file")
@click.argument("output_video")
@click.option("--aes", is_flag=True)
@click.option("--password", default=None)
@click.option("--ecc", is_flag=True)
def encode(input_file, output_video, aes, password, ecc):
    encode_file(input_file, output_video, aes, password, ecc)

@cli.command()
@click.argument("video")
@click.argument("output_file")
@click.option("--password", default=None)
def decode(video, output_file, password):
    decode_video(video, output_file, password)

if __name__ == "__main__":
    cli()
