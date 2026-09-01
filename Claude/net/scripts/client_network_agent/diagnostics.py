from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass
class CommandResult:
    name: str
    command: list[str]
    returncode: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool = False
    skipped: bool = False
    reason: str | None = None


def run_diagnostics(
    target: str,
    output_dir: Path,
    timeout_seconds: int = 20,
    deep: bool = False,
    include_http_body: bool = True,
) -> dict:
    started = datetime.now(timezone.utc)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = started.strftime("%Y%m%dT%H%M%SZ")
    safe_target = _safe_name(target)

    target_info = _parse_target(target)
    commands = _build_plan(target_info, deep=deep)
    command_results = [_run_command(item[0], item[1], timeout_seconds) for item in commands]

    python_checks = {
        "system": _system_snapshot(),
        "dns": _dns_check(target_info["host"]),
        "tcp": _tcp_check(target_info["host"], target_info["port"], timeout_seconds),
    }
    if target_info["url"]:
        python_checks["http"] = _http_check(target_info["url"], timeout_seconds, include_http_body)

    evidence = {
        "agent": "client-network-agent",
        "version": "0.1.0",
        "started_utc": started.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "target": target_info,
        "summary": _summary(target_info, python_checks, command_results),
        "python_checks": python_checks,
        "commands": [asdict(result) for result in command_results],
    }

    json_path = output_dir / f"client-network-agent-{run_id}-{safe_target}.json"
    text_path = output_dir / f"client-network-agent-{run_id}-{safe_target}.txt"
    json_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    text_path.write_text(_render_text(evidence), encoding="utf-8")

    evidence["files"] = {"json": str(json_path.resolve()), "text": str(text_path.resolve())}
    return evidence


def _parse_target(target: str) -> dict:
    value = target.strip()
    parsed = urlparse(value if "://" in value else f"//{value}", scheme="https")
    is_url = "://" in value
    host = parsed.hostname or value.split("/")[0].split(":")[0]
    scheme = parsed.scheme if is_url else None
    port = parsed.port
    if port is None:
        port = 443 if scheme == "https" else 80 if scheme == "http" else 443
    return {
        "raw": target,
        "url": value if is_url else None,
        "host": host,
        "port": port,
        "scheme": scheme,
    }


def _build_plan(target: dict, deep: bool) -> list[tuple[str, list[str]]]:
    system = platform.system().lower()
    host = target["host"]
    plan: list[tuple[str, list[str]]] = []

    if system == "windows":
        plan.extend(
            [
                ("ip_configuration", ["ipconfig", "/all"]),
                ("route_table", ["route", "print"]),
                ("interface_index", ["netsh", "interface", "ipv4", "show", "interfaces"]),
                ("dns_cache", ["ipconfig", "/displaydns"]),
                ("arp_cache", ["arp", "-a"]),
                ("active_connections", ["netstat", "-ano"]),
                ("ping", ["ping", "-n", "4", host]),
                ("traceroute", ["tracert", "-d", host]),
                ("nslookup", ["nslookup", host]),
            ]
        )
        if deep:
            plan.append(("pathping", ["pathping", "-n", host]))
    elif system == "darwin":
        plan.extend(
            [
                ("interfaces", ["ifconfig"]),
                ("route_table", ["netstat", "-rn"]),
                ("dns_config", ["scutil", "--dns"]),
                ("hardware_ports", ["networksetup", "-listallhardwareports"]),
                ("arp_cache", ["arp", "-a"]),
                ("socket_summary", ["netstat", "-an"]),
                ("ping", ["ping", "-c", "4", host]),
                ("traceroute", ["traceroute", "-n", host]),
                ("dns_lookup", ["nslookup", host]),
                ("disk_iostat", ["iostat", "-d", "1", "3"]),
            ]
        )
    else:
        plan.extend(
            [
                ("interfaces", ["ip", "addr"]),
                ("route_table", ["ip", "route"]),
                ("dns_resolver", ["sh", "-c", "resolvectl status 2>/dev/null || cat /etc/resolv.conf"]),
                ("link_status", ["sh", "-c", "nmcli device status 2>/dev/null || true"]),
                ("arp_neighbors", ["ip", "neigh"]),
                ("socket_summary", ["ss", "-s"]),
                ("ping", ["ping", "-c", "4", host]),
                ("tracepath", ["sh", "-c", 'tracepath "$1" 2>/dev/null || traceroute -n "$1"', "sh", host]),
                ("dns_lookup", ["sh", "-c", 'getent hosts "$1"; nslookup "$1" 2>/dev/null || true', "sh", host]),
                ("disk_iostat", ["sh", "-c", "iostat -dx 1 3 2>/dev/null || true"]),
            ]
        )

    if target["url"]:
        plan.append(("curl_timing", _curl_command(target["url"])))
    return plan


def _curl_command(url: str) -> list[str]:
    format_string = (
        "dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} "
        "ttfb=%{time_starttransfer} total=%{time_total} code=%{http_code} remote=%{remote_ip}\n"
    )
    return ["curl", "-L", "-I", "--max-time", "20", "-w", format_string, url]


def _run_command(name: str, command: list[str], timeout_seconds: int) -> CommandResult:
    executable = command[0]
    if executable not in {"sh"} and shutil.which(executable) is None:
        return CommandResult(
            name=name,
            command=command,
            returncode=None,
            duration_ms=0,
            stdout="",
            stderr="",
            skipped=True,
            reason=f"{executable} not found",
        )

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            errors="replace",
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        return CommandResult(
            name=name,
            command=command,
            returncode=completed.returncode,
            duration_ms=duration_ms,
            stdout=completed.stdout[-20000:],
            stderr=completed.stderr[-8000:],
        )
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - started) * 1000)
        return CommandResult(
            name=name,
            command=command,
            returncode=None,
            duration_ms=duration_ms,
            stdout=(exc.stdout or "")[-20000:] if isinstance(exc.stdout, str) else "",
            stderr=(exc.stderr or "")[-8000:] if isinstance(exc.stderr, str) else "",
            timed_out=True,
            reason=f"Timed out after {timeout_seconds}s",
        )


def _system_snapshot() -> dict:
    disk = shutil.disk_usage(Path.cwd())
    snapshot = {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "cwd_disk_total_gb": round(disk.total / 1024**3, 2),
        "cwd_disk_used_gb": round(disk.used / 1024**3, 2),
        "cwd_disk_free_gb": round(disk.free / 1024**3, 2),
    }
    if hasattr(os, "getloadavg"):
        snapshot["load_average"] = os.getloadavg()
    return snapshot


def _dns_check(host: str) -> dict:
    started = time.monotonic()
    try:
        records = socket.getaddrinfo(host, None)
        addresses = sorted({item[4][0] for item in records})
        return {"ok": True, "duration_ms": _elapsed_ms(started), "addresses": addresses}
    except OSError as exc:
        return {"ok": False, "duration_ms": _elapsed_ms(started), "error": str(exc)}


def _tcp_check(host: str, port: int, timeout_seconds: int) -> dict:
    started = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return {"ok": True, "duration_ms": _elapsed_ms(started), "host": host, "port": port}
    except OSError as exc:
        return {
            "ok": False,
            "duration_ms": _elapsed_ms(started),
            "host": host,
            "port": port,
            "error": str(exc),
        }


def _http_check(url: str, timeout_seconds: int, include_body: bool) -> dict:
    started = time.monotonic()
    request = Request(url, method="GET", headers={"User-Agent": "client-network-agent/0.1"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            body = response.read(4096 if include_body else 0)
            return {
                "ok": True,
                "duration_ms": _elapsed_ms(started),
                "status": response.status,
                "headers": dict(response.headers.items()),
                "body_sample_bytes": len(body),
            }
    except Exception as exc:  # urllib raises several network-specific exception types.
        return {"ok": False, "duration_ms": _elapsed_ms(started), "error": repr(exc)}


def _summary(target: dict, checks: dict, commands: Iterable[CommandResult]) -> dict:
    failed_commands = [item.name for item in commands if item.returncode not in (0, None)]
    skipped_commands = [item.name for item in commands if item.skipped]
    return {
        "target": target["raw"],
        "host": target["host"],
        "port": target["port"],
        "dns_ok": checks["dns"]["ok"],
        "tcp_ok": checks["tcp"]["ok"],
        "http_ok": checks.get("http", {}).get("ok"),
        "failed_commands": failed_commands,
        "skipped_commands": skipped_commands,
    }


def _render_text(evidence: dict) -> str:
    lines = [
        "Client Network Agent Evidence",
        f"Started UTC: {evidence['started_utc']}",
        f"Finished UTC: {evidence['finished_utc']}",
        "",
        "Summary",
        json.dumps(evidence["summary"], indent=2),
        "",
        "Python Checks",
        json.dumps(evidence["python_checks"], indent=2),
        "",
        "Command Evidence",
    ]
    for command in evidence["commands"]:
        lines.extend(
            [
                "",
                f"## {command['name']}",
                f"Command: {' '.join(command['command'])}",
                f"Return code: {command['returncode']}",
                f"Duration ms: {command['duration_ms']}",
                f"Skipped: {command['skipped']}",
                f"Timed out: {command['timed_out']}",
                f"Reason: {command['reason']}",
                "-- stdout --",
                command["stdout"],
                "-- stderr --",
                command["stderr"],
            ]
        )
    return "\n".join(lines)


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _safe_name(value: str) -> str:
    allowed = [char.lower() if char.isalnum() else "-" for char in value]
    return "-".join("".join(allowed).split("-"))[:80] or "target"
