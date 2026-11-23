"""Capture the four live fixtures and verify the release checker's results."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
CHECKER = ROOT.parents[1] / "skills" / "erikthiart-seo-release-check" / "scripts" / "check_release.py"
EXPECTED_FAILURES = {
    "locale": set(),
    "archive": set(),
    "manuals": {("route", "/manual-old?source=mail"), ("route", "/docs/manual.pdf"), ("robots", "/docs/wiring")},
    "launch": {("route", "/products/not-a-real-product"), ("route", "/assets/sensor.png"), ("rendered", "/products/sensor")},
}


def check_case(case, origin, manifest, browser, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for item in manifest["routes"]:
        if "rendered" not in item:
            continue
        with TemporaryDirectory() as profile, (directory / item["rendered"]["file"]).open("w") as html:
            command = [
                browser, "--headless", "--disable-background-networking", "--disable-component-update",
                "--no-first-run", f"--user-data-dir={profile}", "--dump-dom", origin + item["path"],
            ]
            subprocess.run(command, stdout=html, stderr=subprocess.DEVNULL, check=True, timeout=30)

    manifest_path = directory / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    command = [sys.executable, str(CHECKER), origin, str(manifest_path), "--rendered-dir", str(directory)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=45)
    (directory / "report.json").write_text(result.stdout)
    report = json.loads(result.stdout)
    failures = {(check["kind"], check["path"]) for check in report["checks"] if check.get("mismatches")}
    expected = EXPECTED_FAILURES[case]
    expected_exit = 1 if expected else 0
    if result.returncode != expected_exit or failures != expected:
        raise RuntimeError(f"{case} unexpected release result. See {directory / 'report.json'}")
    print(f"{case}: expected exit {result.returncode}, {len(failures)} failing checks")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origins", type=Path, help="Origins JSON written by staging.py")
    parser.add_argument("--browser", required=True, help="Path to Chrome or Chromium")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    origins = json.loads(args.origins.read_text())
    contracts = json.loads((ROOT / "contracts.json").read_text())

    for case, contract in contracts.items():
        origin = origins[case]
        manifest = json.loads(json.dumps(contract).replace("{{ORIGIN}}", origin))
        check_case(case, origin, manifest, args.browser, args.output / case)


if __name__ == "__main__":
    main()
