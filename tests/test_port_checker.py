import socket
import threading
from port_checker import check_port, validate_port, check_port_range


def test_validate_port():
    assert validate_port("80") == 80


def test_invalid_port():
    try:
        validate_port("70000")
    except ValueError as exc:
        assert "between 1 and 65535" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_open_local_port():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]
    thread = threading.Thread(target=lambda: server.accept()[0].close(), daemon=True)
    thread.start()
    try:
        result = check_port("127.0.0.1", port, 0.5)
        assert result["status"] == "Open"
        assert result["latency_ms"] >= 0
    finally:
        server.close()


def test_range_limit():
    try:
        check_port_range("127.0.0.1", 1, 101, 0.1)
    except ValueError as exc:
        assert "no more than 100" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
