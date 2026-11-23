"""
Runs a framework's test app as a local server for the duration of a test.
"""

import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]

STARTUP_TIMEOUT_S = 120


def free_port() -> int:
    """
    Returns:
        A TCP port on the loopback interface that is free at the time of the call.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


# The app is on the loopback interface, so the probe ignores any proxy set in
# the environment (http_proxy), which would otherwise receive the request.
_DIRECT = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _ready(url: str) -> bool:
    try:
        with _DIRECT.open(url, timeout=5) as response:
            return response.status == 200
    except (urllib.error.URLError, ConnectionError, OSError):
        return False


@contextmanager
def running_app(
    args: List[str],
    cwd: Path,
    port: int,
    ready_path: str = "/",
    env: Optional[Dict[str, str]] = None,
) -> Iterator[str]:
    """
    Starts an app server and stops it afterwards.

    The app can import the repository's packages, such as `canvasxpress` and
    `tests.functional.platform.charts`, wherever it runs from.

    Args:
        args: The command that starts the server, listening on port.
        cwd: The directory to run the command in.
        port: The port the server listens on.
        ready_path: A path that answers 200 once the server is ready.
        env: Environment variables to add for the server.

    Yields:
        The server's base URL.

    Raises:
        RuntimeError: If the server exits or does not become ready in time,
            with the end of its output.
    """
    server_env = dict(os.environ)
    server_env["PYTHONPATH"] = os.pathsep.join(
        part for part in [str(REPO_ROOT), server_env.get("PYTHONPATH", "")] if part
    )
    server_env["PYTHONUNBUFFERED"] = "1"
    server_env.update(env or {})

    base_url = f"http://127.0.0.1:{port}"
    # Output goes to a file: a pipe nobody reads can fill and stall the server.
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen(
            args, cwd=str(cwd), env=server_env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            deadline = time.monotonic() + STARTUP_TIMEOUT_S
            while not _ready(base_url + ready_path):
                if process.poll() is not None or time.monotonic() > deadline:
                    log.seek(0)
                    output = log.read().decode("utf-8", "replace")[-4000:]
                    raise RuntimeError(
                        f"{' '.join(args)} did not start (exit code"
                        f" {process.poll()}):\n{output}"
                    )
                time.sleep(0.5)

            yield base_url

        finally:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=15)


def python_command(*args: str) -> List[str]:
    """
    Returns:
        A command that runs the current Python interpreter with args.
    """
    return [sys.executable, *args]
