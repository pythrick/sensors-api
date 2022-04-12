import asyncio
import logging
from typing import Optional

import typer
import uvicorn
from typer import Option

from config import settings

from sensors_api.exceptions import InvalidCredentials
from sensors_api.scripts import credentials, simulator

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)

app = typer.Typer()


@app.command()
def create_client_account(description: str = Option(..., help="Account description")):
    response = asyncio.run(credentials.create_client_account(description))
    typer.echo(f"Client Description: {response.description}")
    typer.echo(f"Client ID: {response.client_id}")
    typer.echo(f"Client Secret: {response.client_secret}")


@app.command()
def validate_credentials(
    client_id: str = Option(..., help="Client ID"), client_secret: str = Option(..., help="Client Secret")
):
    try:
        account = asyncio.run(credentials.validate_credentials(client_id, client_secret))
        typer.echo(f"Valid credentials for '{account.description}'.")
    except InvalidCredentials:
        typer.echo(f"Invalid credentials for '{client_id}'.")


@app.command()
def run_simulator(
    devices: int = Option(10, min=10, help="Number of devices to simulate"),
    streaming_interval: Optional[int] = Option(
        None, help="If defined, it will set the same streaming interval for all devices."
    ),
):
    """Start devices simulator to create records in Sensors API."""
    asyncio.run(simulator.start_simulator(devices, streaming_interval))


@app.command(name="runserver")
def run_server(
    host: str = settings.host,
    port: int = settings.port,
    debug: bool = settings.debug,
    reload: bool = settings.debug,
):
    uvicorn.run(
        "sensors_api.api:app",
        debug=debug,
        reload=reload,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    app()
