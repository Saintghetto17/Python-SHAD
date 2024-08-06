import click
from steganography_tool import decode_message, encode_message
from steganography_tool.utils import get_base_file, read_file, write_file


@click.group()
def cli() -> None:
    pass


# args is the name of tuple for arguments of encode command
@cli.command()
@click.argument('args', nargs=2)
def encode(args: tuple[str, str]) -> None:
    file = args[0]
    message = args[1]
    data_base = get_base_file()
    encoded_image_data = encode_message(data_base, message)
    write_file(encoded_image_data, file)
    pass


@cli.command()
@click.argument('filename')
def decode(filename: str) -> None:
    click.echo(decode_message(read_file(filename)))
