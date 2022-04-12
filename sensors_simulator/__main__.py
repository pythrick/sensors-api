import asyncio
import logging
from typing import Optional

from typer import Option, Typer

from sensors_simulator.core import Simulator

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)


app = Typer()


@app.command()
def start_simulator(
    devices: int = Option(10, help="Number of devices to start streaming data.", min=10),
    streaming_interval: Optional[int] = Option(None, help="Streaming interval in seconds.", min=0),
    base_url: str = Option("http://0.0.0.0:8000", help="Sensors API base URL."),
):
    simulator = Simulator(
        base_url=base_url,
        devices_num=devices,
        streaming_interval=streaming_interval,
    )
    asyncio.run(simulator.start())


def main():
    app()


if __name__ == "__main__":
    main()
