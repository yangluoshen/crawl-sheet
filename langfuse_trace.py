import os
import base64
from opentelemetry.sdk.trace import TracerProvider
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

LANGFUSE_PUBLIC_KEY=os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY=os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_AUTH=base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()
OTEL_EXPORTER_OTLP_ENDPOINT="https://us.cloud.langfuse.com/api/public/otel"

def init_trace():
    
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"
    print(os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"])
    print (os.environ["OTEL_EXPORTER_OTLP_HEADERS"])
    print(LANGFUSE_PUBLIC_KEY)
    print(LANGFUSE_SECRET_KEY)
    
    trace_provider = TracerProvider()
    # trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(
        headers={"Authorization": f"Basic {LANGFUSE_AUTH}"},
    )))

    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)