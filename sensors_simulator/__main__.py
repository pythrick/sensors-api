import asyncio
import logging
from typing import Optional

from typer import Option, Typer

from config import settings
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

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource(attributes={"service.name": "sensors-simulator"})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.collector_endpoint, insecure=True)
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

    app()

    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

    HTTPXClientInstrumentor().instrument()


if __name__ == "__main__":
    main()
