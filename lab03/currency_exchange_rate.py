from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests

DATE_FORMAT = "%Y-%m-%d"
TIMEOUT_SECONDS = 10

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
LOG_FILE = ROOT_DIR / "error.log"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch currency exchange rate and save response to JSON."
    )
    parser.add_argument("from_currency", help="Currency code to convert from (e.g. USD)")
    parser.add_argument("to_currency", help="Currency code to convert to (e.g. EUR)")
    parser.add_argument("date", help=f"Date in {DATE_FORMAT} format")
    parser.add_argument("--api-key", required=True, help="API key for the service")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8089/",
        help="Base URL of the service (default: http://localhost:8080/)",
    )
    return parser.parse_args(argv)


def log_error(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} - {message}\n")


def fetch_exchange_rate(params: dict[str, Any]) -> Dict[str, Any]:
    url = params["base_url"].rstrip("/") + "/"
    query = {"from": params["from_currency"], "to": params["to_currency"], "date": params["date"]}
    payload = {"key": params["api_key"]}

    try:
        response = requests.post(url, params=query, data=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"HTTP request failed: {exc}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError("Invalid JSON in response.") from exc

    if "error" in data and data["error"]:
        raise RuntimeError(f"Service returned an error: {data['error']}")

    return data


def save_response(params: dict[str, Any], data: Dict[str, Any]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{params['from_currency']}_{params['to_currency']}_{params['date']}.json"
    destination = DATA_DIR / filename
    with destination.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    return destination


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)

        # валидация даты
        try:
            datetime.strptime(args.date, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid date '{args.date}', expected format {DATE_FORMAT}")

        params = {
            "from_currency": args.from_currency.upper(),
            "to_currency": args.to_currency.upper(),
            "date": args.date,
            "api_key": args.api_key,
            "base_url": args.base_url,
        }

        data = fetch_exchange_rate(params)
        out_file = save_response(params, data)
        rate = data.get("data", {}).get("rate")

        print(
            f"Saved exchange rate {params['from_currency']} -> {params['to_currency']} "
            f"for {params['date']} (rate: {rate}) to {out_file}"
        )
        return 0

    except Exception as exc:
        msg = str(exc)
        print(f"Error: {msg}", file=sys.stderr)
        log_error(msg)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
