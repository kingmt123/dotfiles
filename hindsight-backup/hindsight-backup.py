#!/usr/bin/env python3
"""
Hindsight Memory Backup Script
Exports all memories, config, and stats from Hindsight API to JSON files.
Creates timestamped export directories.
"""

import urllib.request, json, os, sys
from datetime import datetime

HINDSIGHT_BASE = "http://localhost:8888/v1/default/banks"
BANK_ID = "hermes"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")

def api_get(path):
    with urllib.request.urlopen(f"{HINDSIGHT_BASE}/{BANK_ID}{path}", timeout=15) as resp:
        return json.loads(resp.read())

def api_post(path, data=None):
    payload = json.dumps(data or {}).encode()
    req = urllib.request.Request(
        f"{HINDSIGHT_BASE}/{BANK_ID}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def save_json(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {filename} ({len(json.dumps(data))} bytes)")
    return path

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    global OUTPUT_DIR
    OUTPUT_DIR = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Hindsight Backup — {timestamp}")
    print(f"Output: {OUTPUT_DIR}\n")

    # 1. Bank export (template with config + mental models)
    print("[1/6] Bank export...")
    try:
        data = api_get("/export")
        save_json(data, "bank-export.json")
    except Exception as e:
        print(f"  ✗ bank-export: {e}")

    # 2. Bank config
    print("[2/6] Bank config...")
    try:
        data = api_get("/config")
        save_json(data, "bank-config.json")
    except Exception as e:
        print(f"  ✗ bank-config: {e}")

    # 3. Bank profile (disposition, mission)
    print("[3/6] Bank profile...")
    try:
        data = api_get("/profile")
        save_json(data, "bank-profile.json")
    except Exception as e:
        print(f"  ✗ bank-profile: {e}")

    # 4. Stats
    print("[4/6] Bank stats...")
    try:
        data = api_get("/stats")
        save_json(data, "bank-stats.json")
    except Exception as e:
        print(f"  ✗ bank-stats: {e}")

    # 5. Tags
    print("[5/6] Tags...")
    try:
        data = api_get("/tags")
        save_json(data, "tags.json")
    except Exception as e:
        print(f"  ✗ tags: {e}")

    # 6. All memories (recall with broad queries to get everything)
    print("[6/6] All memories...")
    all_memories = []
    seen_ids = set()

    queries = [
        "kingmt user profile identity",
        "grasp-sim-pipeline project robotics",
        "paper review academic AV",
        "hindsight memory backup",
        "development environment tools workflow",
        "python uv code review preferences",
        "hermes claude code AI assistant",
    ]

    for query in queries:
        try:
            result = api_post("/memories/recall", {
                "query": query,
                "max_results": 200
            })
            items = result.get("results", result.get("memories", []))
            for m in items:
                mid = m.get("id", "")
                if mid and mid not in seen_ids:
                    seen_ids.add(mid)
                    all_memories.append(m)
        except Exception as e:
            print(f"  ✗ recall('{query}'): {e}")

    save_json({
        "total": len(all_memories),
        "exported_at": timestamp,
        "memories": all_memories
    }, "memories.json")

    # Summary
    print(f"\n=== Summary ===")
    print(f"  Total memories exported: {len(all_memories)}")
    print(f"  Total files: {len(os.listdir(OUTPUT_DIR))}")
    print(f"  Export directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
