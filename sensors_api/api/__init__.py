import logging

from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from config import settings

from sensors_api.api.v1 import v1_router
from sensors_api.db.connection import engine, init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sensors API",
    contact={"name": "Patrick Rodrigues", "email": "patrick.pwall@gmail.com"},
    license_info={"name": "MIT"},
)

app.include_router(v1_router)

if settings.enable_trace:
    from opentelemetry import trace
    from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource(attributes={"service.name": "sensors-api"})

    exporter = OTLPSpanExporter(endpoint=settings.collector_endpoint, insecure=True)

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)

    FastAPIInstrumentor.instrument_app(app)
    # SQLAlchemyInstrumentor().instrument(engine=engine)

    if "asyncpg" in settings.database_url:
        AsyncPGInstrumentor().instrument()


@app.on_event("startup")
async def on_startup():
    from sensors_api.db.models.device import Device  # noqa
    from sensors_api.db.models.record import Record  # noqa

    logger.info("Initializing database...")
    await init_db()


@app.get("/ping")
async def ping():
    """Provide a simple API healthcheck."""
    return {"ping": "pong!"}
