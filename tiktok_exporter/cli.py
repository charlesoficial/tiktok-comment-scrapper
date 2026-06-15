from __future__ import annotations

import click

from .client import TikTokClientError
from .exporter import export_comments
from .utils import VideoIdError

APP_NAME = "TikTok Comments Exporter"
VERSION = "1.0.0"


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
    default=None,
    type=click.IntRange(min=1),
    help="Limita a quantidade de comentarios. Sem isso, coleta todos.",
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
    type=click.Choice(["json", "csv", "txt", "xlsx", "both", "all"]),
    default="json",
    show_default=True,
    help="Formato de saida (both = json+csv, all = json+csv+txt+xlsx).",
)
@click.option(
    "--quiet/--verbose",
    default=False,
    show_default=True,
    help="Silencia as mensagens de progresso.",
)
def main(
    video: str,
    limit: int | None,
    output: str,
    replies: bool,
    pretty: bool,
    file_format: str,
    quiet: bool,
) -> None:
    def progress(message: str) -> None:
        if not quiet:
            click.echo(message, err=True)

    try:
        file_paths = export_comments(
            video,
            limit=limit,
            output_dir=output,
            include_replies=replies,
            pretty=pretty,
            file_format=file_format,
            progress=progress,
        )
    except (TikTokClientError, VideoIdError) as exc:
        raise click.ClickException(str(exc)) from exc

    for file_path in file_paths:
        click.echo(f"Arquivo salvo em: {file_path}")
