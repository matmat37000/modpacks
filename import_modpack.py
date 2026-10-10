#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


def main():
    json_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("modpack.json")

    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    files = data.get("files", [])
    urls = [
        url
        for entry in files
        for url in entry.get("downloads", [])
        if url
    ]

    print(f"Found {len(urls)} download URLs.\n")

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] Running: packwiz modrinth add {url}")

        try:
            result = subprocess.run(
                ["packwiz", "modrinth", "add", url],
                input="n\n",
                text=True,
                check=False,
            )

            if result.returncode != 0:
                print(f"Command failed with exit code {result.returncode}: {url}")

        except FileNotFoundError:
            print("Error: packwiz was not found. Make sure it is installed and on PATH.")
            return

    print("\nDone!")


if __name__ == "__main__":
    main()
