#!/usr/bin/env python3
"""render-artifact — turn a result into a clean IMAGE for X (LaTeX doesn't
render in tweets, so every final result is posted as a rendered picture).

Two engines:
  html   <in.html> <out.png> [width]   headless-chromium screenshot of an HTML
                                        page (use inline/vendored KaTeX or MathJax
                                        for beautiful math; fully self-contained).
  verify <img.png>                      sanity-check a render: exists, non-trivial
                                        size, not blank/monochrome. Exit 0 = good.

The `html` engine tries Playwright's chromium first (baked into the sandbox),
then a system `chromium`/`chromium-browser --headless`. Prints JSON.

For simple formulas/tables/plots/graphs, matplotlib (mathtext, offline) is the
reliable default — see doctrine; this tool is for richer typeset layouts (the
DGG-style certificate card, a construction diagram, a theorem statement).
"""
import json
import os
import subprocess
import sys


def die(m):
    print(json.dumps({"ok": False, "error": str(m)}))
    sys.exit(1)


def render_html(html_path, out_png, width=1200):
    html_path = os.path.abspath(html_path)
    out_png = os.path.abspath(out_png)
    url = "file://" + html_path
    # 1) Playwright chromium (baked)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": int(width), "height": 200},
                            device_scale_factor=2)
            pg.goto(url, wait_until="networkidle")
            pg.wait_for_timeout(400)
            pg.screenshot(path=out_png, full_page=True)
            b.close()
        return out_png
    except Exception as e:
        last = f"playwright: {e}"
    # 2) system chromium headless
    for exe in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        try:
            subprocess.run(
                [exe, "--headless=new", "--no-sandbox", "--hide-scrollbars",
                 f"--screenshot={out_png}", f"--window-size={int(width)},1200",
                 "--force-device-scale-factor=2", "--default-background-color=00000000",
                 url],
                check=True, capture_output=True, timeout=90)
            if os.path.exists(out_png):
                return out_png
        except Exception as e:
            last = f"{exe}: {e}"
    die(f"no working chromium ({last}); install via harness or use matplotlib")


def verify(img):
    if not os.path.exists(img):
        die("missing")
    size = os.path.getsize(img)
    if size < 2000:
        die(f"too small ({size}b) — likely blank")
    try:
        from PIL import Image
        im = Image.open(img).convert("RGB")
        colors = im.getcolors(maxcolors=100000)
        if colors and len(colors) < 3:
            die("blank/monochrome — render failed")
        w, h = im.size
        if w < 100 or h < 40:
            die(f"degenerate dims {w}x{h}")
    except ImportError:
        pass  # PIL optional; size check already passed
    print(json.dumps({"ok": True, "path": os.path.abspath(img), "bytes": size}))


def main():
    if len(sys.argv) < 3:
        die(__doc__)
    cmd = sys.argv[1]
    if cmd == "html":
        out = render_html(sys.argv[2], sys.argv[3],
                          sys.argv[4] if len(sys.argv) > 4 else 1200)
        print(json.dumps({"ok": True, "path": out}))
    elif cmd == "verify":
        verify(sys.argv[2])
    else:
        die(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
