import json
import logging

from localrestaurantmenus_project.log_config import CloudRunJSONFormatter


def _format(record):
    return json.loads(CloudRunJSONFormatter().format(record))


def test_basic_record_emits_severity_and_message():
    rec = logging.LogRecord(
        name="myapp", level=logging.INFO, pathname="x.py", lineno=1,
        msg="hello %s", args=("world",), exc_info=None,
    )
    payload = _format(rec)
    assert payload["severity"] == "INFO"
    assert payload["message"] == "hello world"
    assert payload["logger"] == "myapp"


def test_warning_and_error_levels_map_to_cloud_severity():
    for level, expected in [
        (logging.WARNING, "WARNING"),
        (logging.ERROR, "ERROR"),
        (logging.CRITICAL, "CRITICAL"),
    ]:
        rec = logging.LogRecord("x", level, "x.py", 1, "m", None, None)
        assert _format(rec)["severity"] == expected


def test_exception_traceback_is_included():
    try:
        raise ValueError("boom")
    except ValueError:
        import sys
        rec = logging.LogRecord(
            "x", logging.ERROR, "x.py", 1, "failed", None, sys.exc_info()
        )
    payload = _format(rec)
    assert payload["severity"] == "ERROR"
    assert "ValueError: boom" in payload["exception"]
    assert "Traceback" in payload["exception"]


def test_extra_fields_are_promoted():
    rec = logging.LogRecord("x", logging.INFO, "x.py", 1, "m", None, None)
    rec.path = "/ehsanis-hot-kabob/"
    rec.status = 200
    payload = _format(rec)
    assert payload["path"] == "/ehsanis-hot-kabob/"
    assert payload["status"] == 200


def test_output_is_single_line_json():
    rec = logging.LogRecord("x", logging.INFO, "x.py", 1, "line1\nline2", None, None)
    out = CloudRunJSONFormatter().format(rec)
    assert "\n" not in out
    assert json.loads(out)["message"] == "line1\nline2"
