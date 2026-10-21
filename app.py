from flask import Flask, render_template, request
from port_checker import check_port, check_port_range, validate_target, validate_port
from flask import request, render_template
from port_checker import check_local_port

app = Flask(__name__)
app.config["SECRET_KEY"] = "development-only-change-me"


@app.get("/")
def index():
    return render_template("index.html", result=None, results=None, error=None)


@app.post("/check")
def check():
    target = request.form.get("target", "").strip()
    port_text = request.form.get("port", "").strip()
    timeout_text = request.form.get("timeout", "1.0").strip()
    try:
        validate_target(target)
        port = validate_port(port_text)
        timeout = float(timeout_text)
        if not 0.1 <= timeout <= 5:
            raise ValueError("Timeout must be between 0.1 and 5 seconds.")
        result = check_port(target, port, timeout)
        return render_template("index.html", result=result, results=None, error=None)
    except (ValueError, OSError) as exc:
        return render_template("index.html", result=None, results=None, error=str(exc)), 400


@app.post("/range")
def range_check():
    target = request.form.get("target", "").strip()
    start_text = request.form.get("start_port", "").strip()
    end_text = request.form.get("end_port", "").strip()
    timeout_text = request.form.get("timeout", "0.5").strip()
    try:
        validate_target(target)
        start_port = validate_port(start_text)
        end_port = validate_port(end_text)
        timeout = float(timeout_text)
        if not 0.1 <= timeout <= 3:
            raise ValueError("Timeout must be between 0.1 and 3 seconds for a range check.")
        if end_port < start_port:
            raise ValueError("End port must be greater than or equal to start port.")
        if end_port - start_port + 1 > 100:
            raise ValueError("For safety, check no more than 100 ports per request.")
        results = check_port_range(target, start_port, end_port, timeout)
        opened = sum(1 for item in results if item["status"] == "Open")
        summary = {
            "target": target,
            "start_port": start_port,
            "end_port": end_port,
            "checked": len(results),
            "open_count": opened,
            "closed_count": sum(1 for item in results if item["status"] == "Closed"),
            "timeout_count": sum(1 for item in results if item["status"] == "Timeout"),
            "total_ms": round(sum(item["latency_ms"] for item in results), 2),
        }
        return render_template("index.html", result=None, results=results, summary=summary, error=None)
    except (ValueError, OSError) as exc:
        return render_template("index.html", result=None, results=None, summary=None, error=str(exc)), 400

@app.route("/local-port-check", methods=["GET", "POST"])
def local_port_check():
    result = None
    port_value = ""

    if request.method == "POST":
        port_value = request.form.get("port", "").strip()

        try:
            if not port_value.isdigit():
                raise ValueError("Enter a valid port number.")

            port = int(port_value)
            result = check_local_port(port)

        except ValueError as exc:
            result = {
                "status": "ERROR",
                "message": str(exc)
            }

    return render_template(
        "local_port.html",
        result=result,
        port=port_value
    )

if __name__ == "__main__":
    # Local development server. Do not expose this demo app to the public internet.
    app.run(host="127.0.0.1", port=5001, debug=False)
