import click
from .encoder import encode_file
from .decoder import decode_video

@click.group()
def cli():
    """VideoBin+ CLI - Almacena archivos en video usando 2 colores"""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_video", type=click.Path())
@click.option("--aes", is_flag=True, help="Habilitar cifrado AES-256")
@click.option("--password", default=None, help="Contraseña para AES")
@click.option("--ecc", is_flag=True, help="Habilitar corrección de errores Reed-Solomon")
def encode(input_file, output_video, aes, password, ecc):
    """Codifica un archivo a video"""
    if aes and not password:
        raise click.ClickException("Se requiere --password cuando se usa --aes")
    
    click.echo(f"Codificando {input_file} -> {output_video}")
    encode_file(input_file, output_video, aes, password, ecc)
    click.echo("✓ Codificación completada")

@cli.command()
@click.argument("video", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--password", default=None, help="Contraseña si el video está cifrado")
def decode(video, output_file, password):
    """Decodifica un video a archivo"""
    click.echo(f"Decodificando {video} -> {output_file}")
    decode_video(video, output_file, password)
    click.echo("✓ Decodificación completada")

if __name__ == "__main__":
    cli()
