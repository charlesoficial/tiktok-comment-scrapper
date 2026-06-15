from __future__ import annotations

import click

from .client import TikTokClientError
from .exporter import export_comments
from .utils import VideoIdError

APP_NAME = "TikTok Comments Exporter"
VERSION = "3.0.0"


@click.command(help="Exporta comentarios publicos de videos do TikTok para JSON.")
@click.version_option(version=VERSION, prog_name=APP_NAME)
@click.option(
    "--video",
    "--aweme-id",
    "video",
    required=True,
    help="ID ou URL do video do TikTok.",
)
@click.option(
    "--limit",
    "--size",
    "-s",
    default=50,
    show_default=True,
    type=click.IntRange(min=1),
    help="Quantidade maxima de comentarios.",
)
@click.option(
    "--output",
    "-o",
    default="data",
    show_default=True,
    help="Pasta onde o JSON sera salvo.",
)
@click.option(
    "--replies/--no-replies",
    default=True,
    show_default=True,
    help="Inclui replies dos comentarios.",
)
@click.option(
    "--pretty/--compact",
    default=True,
    show_default=True,
    help="Formata o JSON com indentacao.",
)
@click.option(
    "--format",
    "file_format",
    type=click.Choice(["json", "csv", "both"]),
    default="json",
    show_default=True,
    help="Formato de saida.",
)
def main(
    video: str,
    limit: int,
    output: str,
    replies: bool,
    pretty: bool,
    file_format: str,
) -> None:
    try:
        file_paths = export_comments(
            video,
            limit=limit,
            output_dir=output,
            include_replies=replies,
            pretty=pretty,
            file_format=file_format,
        )
    except (TikTokClientError, VideoIdError) as exc:
        raise click.ClickException(str(exc)) from exc

    for file_path in file_paths:
        click.echo(f"Arquivo salvo em: {file_path}")
