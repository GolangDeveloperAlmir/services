"""Optional FastAPI request tracing with OTLP gRPC export."""

import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings


logger = logging.getLogger(__name__)


def configure_telemetry(app: FastAPI) -> TracerProvider | None:
    """Set up FastAPI tracing if an OTLP endpoint is configured."""
    endpoint = settings.otel_exporter_otlp_endpoint
    if not endpoint:
        return None

    service_name = settings.otel_service_name or settings.app_name
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name}),
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)),
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    logger.info(
        "OpenTelemetry tracing enabled",
        extra={"service_name": service_name},
    )
    return provider
