"""Cloud Logging-compatible JSON log formatter for Cloud Run.

Cloud Run captures stdout and forwards each line to Cloud Logging. When the
line is JSON with a top-level ``severity`` field, Cloud Logging parses it as
``jsonPayload`` and surfaces severity correctly in the UI; otherwise it shows
up as a plain ``textPayload``. See:
https://cloud.google.com/logging/docs/structured-logging
"""
import json
import logging
import traceback


_SEVERITY = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL",
}

_RESERVED = frozenset({
    "args", "asctime", "created", "exc_info", "exc_text", "filename",
    "funcName", "levelname", "levelno", "lineno", "message", "module",
    "msecs", "msg", "name", "pathname", "process", "processName",
    "relativeCreated", "stack_info", "thread", "threadName", "taskName",
})


class CloudRunJSONFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "severity": _SEVERITY.get(record.levelno, "DEFAULT"),
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exception"] = "".join(traceback.format_exception(*record.exc_info))

        # Promote anything passed via logger.info(..., extra={"foo": "bar"})
        # into the JSON payload so Cloud Logging indexes it as a field.
        for k, v in record.__dict__.items():
            if k.startswith("_") or k in _RESERVED:
                continue
            try:
                json.dumps(v)
                payload[k] = v
            except (TypeError, ValueError):
                payload[k] = repr(v)

        return json.dumps(payload, default=str)
