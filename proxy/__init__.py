import base64
import os
import random
from pathlib import Path
from typing import Optional

import typer
import uvicorn
from typing_extensions import Annotated

app = typer.Typer()


def version_callback(value: bool):
    if value:
        from open_webui.env import VERSION

        typer.echo(f"Open WebUI version: {VERSION}")
        raise typer.Exit()


@app.command()
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    pass


if __name__ == "__main__":
    app()
