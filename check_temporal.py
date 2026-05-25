"""Check temporal.html rendering state."""
from playwright.sync_api import sync_playwright

console_logs = []
page_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: page_errors.append(str(err)))

    page.goto("http://localhost:8767/temporal.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # give time for fetch + charts

    # Screenshot
    page.screenshot(path="/tmp/temporal_check.png", full_page=True)

    # Check each canvas
    print("=" * 60)
    print("CANVAS CHECK")
    print("=" * 60)
    for cid in ["chart-timelines", "chart-tradeoff", "chart-reversal-time",
                "chart-crisis-1997", "chart-reversal-1997"]:
        loc = page.locator(f"#{cid}")
        cnt = loc.count()
        if cnt == 0:
            print(f"  {cid}: NOT FOUND")
            continue
        box = loc.bounding_box()
        if box is None:
            print(f"  {cid}: present but no bounding box")
        else:
            print(f"  {cid}: found, size {box['width']:.0f}x{box['height']:.0f}")

    # Check findings text
    print("\n" + "=" * 60)
    print("FINDING TEXT CHECK")
    print("=" * 60)
    for fid in ["finding-timelines", "finding-tradeoff", "finding-reversal-time",
                "finding-crisis-1997", "finding-reversal-1997"]:
        loc = page.locator(f"#{fid}")
        cnt = loc.count()
        if cnt > 0:
            text = loc.inner_text()[:120]
            print(f"  {fid}: {text!r}")

    # Hero
    print("\n" + "=" * 60)
    print("HERO CHECK")
    print("=" * 60)
    hero = page.locator(".hero h1").first
    if hero.count() > 0:
        print(f"  H1: {hero.inner_text()!r}")
    else:
        print("  Hero H1: NOT FOUND")

    # Console & errors
    print("\n" + "=" * 60)
    print(f"CONSOLE LOGS ({len(console_logs)})")
    print("=" * 60)
    for log in console_logs[:20]:
        print(f"  {log}")
    print("\n" + "=" * 60)
    print(f"PAGE ERRORS ({len(page_errors)})")
    print("=" * 60)
    for err in page_errors:
        print(f"  {err}")

    browser.close()
print("\nScreenshot: /tmp/temporal_check.png")
