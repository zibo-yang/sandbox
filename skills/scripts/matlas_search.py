#!/usr/bin/env python3
"""Search matlas.ai mathematical literature database or read saved results."""

import argparse
import json
import os
import random
import sys
import time

import httpx

BASE_URL = "https://matlas.ai"
MIN_RESULTS = 10
MAX_RESULTS = 200
DEFAULT_RESULTS = 10
TIMEOUT = 30.0
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/",
}


def _clamp(n):
    return max(MIN_RESULTS, min(MAX_RESULTS, int(n)))


def _build_link(r):
    """Build a URL for a result: DOI link for papers, Google search for books."""
    doi = (r.get("doi") or "").strip()
    if doi:
        if doi.startswith("http://") or doi.startswith("https://"):
            return doi
        return f"https://{doi.lstrip('/')}"
    parts = [p for p in (r.get("title", ""), r.get("authors", "")) if p]
    if parts:
        from urllib.parse import quote
        return f"https://www.google.com/search?q={quote(' '.join(parts))}"
    return ""


def search(query, num_results=DEFAULT_RESULTS):
    """Search matlas.ai and return a list of result dicts (with 'link' added)."""
    query = str(query or "").strip()
    if not query:
        raise ValueError("query must be a non-empty string")

    body = {"query": query, "num_results": _clamp(num_results)}

    with httpx.Client(base_url=BASE_URL, headers=HEADERS, timeout=TIMEOUT) as client:
        last_err = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = client.post("/api/search", json=body)
            except httpx.HTTPError as e:
                last_err = e
                if attempt < MAX_RETRIES:
                    time.sleep(0.75 * (2 ** attempt) * (0.5 + random.random()))
                    continue
                raise RuntimeError(f"Network error: {e}") from e

            if resp.status_code == 200:
                data = resp.json()
                if not isinstance(data, list):
                    raise RuntimeError(f"Unexpected response shape: {type(data).__name__}")
                for r in data:
                    r["link"] = _build_link(r)
                return data

            if (resp.status_code == 429 or resp.status_code >= 500) and attempt < MAX_RETRIES:
                time.sleep(0.75 * (2 ** attempt) * (0.5 + random.random()))
                continue

            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")

        raise RuntimeError(f"Request failed after retries: {last_err}")


def _print_result(idx, r):
    header = f"[{idx}] {r.get('type', '?')}"
    name = r.get("entity_name", "")
    if name:
        header += f" \u00b7 {name}"
    print(header)
    if r.get("title"):
        print(f"    {r['title']}")
    meta = [p for p in (r.get("authors", ""), r.get("journal", ""), r.get("year", "")) if p]
    if meta:
        print(f"    {', '.join(meta)}")
    if r.get("link"):
        print(f"    link: {r['link']}")
    if r.get("statement"):
        stmt = r["statement"].replace("\n", " ")
        if len(stmt) > 500:
            stmt = stmt[:500] + " ..."
        print(f"    {stmt}")
    print()


def _read_jsonl(path, query_filter=None):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if query_filter and query_filter.lower() not in record.get("query", "").lower():
                continue
            q = record.get("query", "")
            results = record.get("results", [])
            print(f"=== {q} ({len(results)} results) ===")
            for i, r in enumerate(results, 1):
                _print_result(i, r)


def main():
    parser = argparse.ArgumentParser(
        description="Search matlas.ai math literature or read saved results."
    )
    parser.add_argument("query", nargs="?", help="Search query string")
    parser.add_argument("-n", "--num-results", type=int, default=DEFAULT_RESULTS,
                        help=f"Number of results ({MIN_RESULTS}-{MAX_RESULTS}, default {DEFAULT_RESULTS})")
    parser.add_argument("-o", "--output", help="Save results to JSONL file (append mode)")
    parser.add_argument("--read", metavar="FILE", help="Read mode: display saved JSONL file")
    parser.add_argument("--query", dest="filter_query", help="Filter --read results by query substring")
    args = parser.parse_args()

    if args.read:
        if not os.path.isfile(args.read):
            print(f"Error: file not found: {args.read}", file=sys.stderr)
            return 1
        _read_jsonl(args.read, args.filter_query)
        return 0

    if not args.query:
        parser.error("query is required in search mode (or use --read for read mode)")

    try:
        results = search(args.query, num_results=args.num_results)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "a") as f:
            f.write(json.dumps(
                {"query": args.query, "results": results},
                ensure_ascii=False,
            ) + "\n")
        print(f"Saved {len(results)} results to {args.output}")
    else:
        print(f"=== {args.query} ({len(results)} results) ===")
        for i, r in enumerate(results, 1):
            _print_result(i, r)

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
