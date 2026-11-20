"""Repeat the six route comparisons with the visual-diff skill's CLI.

Serve app/dist on port 4173 first. Set VISUAL_DIFF_PYTHON to a Python with
playwright, pillow and numpy; install Playwright Chromium in that environment.
Outputs are evidence only; this helper never edits application files.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import os
import subprocess

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / 'compare-normalized.py'
PYTHON = os.environ.get('VISUAL_DIFF_PYTHON', '/tmp/bhr-visual-diff-venv/bin/python')
ROUTES = {
    'expertises': '/expertises',
    'machinebouwers': '/voor-machinebouwers/voor-machinebouwers',
    'proces-productie': '/voor-machinebouwers/proces-productie',
    'service-en-onderhoud': '/service-en-onderhoud',
    'partners': '/over-ons/partners',
    'werken-bij': '/over-ons/werken-bij',
}
OUTPUT = ROOT


def compare(item):
    key, route = item
    out = OUTPUT / key
    out.mkdir(parents=True, exist_ok=True)
    cmd = [PYTHON, str(SKILL), '--reference', 'https://www.bhr-is.nl' + route,
           '--candidate', 'http://127.0.0.1:4173' + route, '--out', str(out),
           '--viewport', 'desktop:1440x900', '--viewport', 'tablet:768x1024',
           '--viewport', 'mobile:390x844', '--dismiss', 'button.cc-allow',
           '--dismiss', '[data-consent="accepted"]', '--wait-until', 'domcontentloaded',
           '--dismiss-cycles', '1', '--wait-ms', '1800', '--lazy-scroll',
           '--scroll-y', '0', '--scroll-wait-ms', '1200',
           '--locale', 'nl-NL', '--timezone', 'Europe/Amsterdam',
           '--color-scheme', 'light', '--fail-on-zoom-mismatch']
    with (out / 'capture.log').open('w') as log:
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    print(f'{key}: exit {result.returncode}; {out / "report.md"}', flush=True)
    return result.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--route', action='append', choices=ROUTES)
    parser.add_argument('--out', type=Path, default=ROOT)
    args = parser.parse_args()
    OUTPUT = args.out.resolve()
    chosen = [(k, v) for k, v in ROUTES.items() if not args.route or k in args.route]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(compare, chosen))
    raise SystemExit(1 if any(results) else 0)
