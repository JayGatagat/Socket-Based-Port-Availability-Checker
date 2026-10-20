"""TCP port availability checks for hosts you own or have permission to test."""
import ipaddress
import socket
import time


def validate_target(target: str) -> str:
    """Validate a hostname/IP and restrict this educational tool to local/private targets."""
    if not target:
        raise ValueError("Enter a hostname or IP address.")
    if any(ch.isspace() for ch in target):
        raise ValueError("Hostname/IP must not contain spaces.")
    try:
        addresses = socket.getaddrinfo(target, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve target '{target}'. Check the hostname.") from exc

    # Allow localhost and private/loopback/link-local IPs only.
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0].split("%")[0])
        if not (ip.is_private or ip.is_loopback or ip.is_link_local):
            raise ValueError(
                "This demo is limited to localhost/private-network targets. "
                "Use a host you own or are authorized to test."
            )
    return target


def validate_port(port_value) -> int:
    try:
        port = int(port_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Port must be an integer from 1 to 65535.") from exc
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    return port


def check_port(target: str, port: int, timeout: float = 1.0) -> dict:
    """Attempt one TCP connection and classify its outcome."""
    validate_target(target)
    port = validate_port(port)
    started = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        code = sock.connect_ex((target, port))
        elapsed = (time.perf_counter() - started) * 1000
        if code == 0:
            status, detail = "Open", "TCP connection succeeded."
        elif code in (getattr(__import__("errno"), "ECONNREFUSED"),):
            status, detail = "Closed", "Connection was refused."
        else:
            status, detail = "Closed", f"Connection failed (OS error {code})."
        return {"target": target, "port": port, "status": status,
                "latency_ms": round(elapsed, 2), "detail": detail}
    except socket.timeout:
        elapsed = (time.perf_counter() - started) * 1000
        return {"target": target, "port": port, "status": "Timeout",
                "latency_ms": round(elapsed, 2), "detail": "No response before timeout."}
    except OSError as exc:
        elapsed = (time.perf_counter() - started) * 1000
        return {"target": target, "port": port, "status": "Error",
                "latency_ms": round(elapsed, 2), "detail": str(exc)}
    finally:
        sock.close()


def check_port_range(target: str, start_port: int, end_port: int, timeout: float = 0.5) -> list:
    """Check a small bounded port range sequentially."""
    validate_target(target)
    start_port = validate_port(start_port)
    end_port = validate_port(end_port)
    if end_port < start_port:
        raise ValueError("End port must be greater than or equal to start port.")
    if end_port - start_port + 1 > 100:
        raise ValueError("For safety, check no more than 100 ports per request.")
    return [check_port(target, port, timeout) for port in range(start_port, end_port + 1)]
