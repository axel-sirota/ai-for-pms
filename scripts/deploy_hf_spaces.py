#!/usr/bin/env python3
"""
Deploy Gradio apps to HuggingFace Spaces.

Usage:
    .venv/bin/python3 scripts/deploy_hf_spaces.py                    # Deploy all
    .venv/bin/python3 scripts/deploy_hf_spaces.py ai-paradigm-picker # Deploy one

Requires: huggingface-cli login (run once before deploying)

Sources:
- https://huggingface.co/docs/hub/en/spaces-sdks-gradio
- https://www.gradio.app/guides/using-hugging-face-integrations
"""

import argparse
import sys
from pathlib import Path

from huggingface_hub import HfApi, create_repo, upload_folder

# All apps to deploy
APPS = [
    # Section 1
    "ai-paradigm-picker",
    "build-vs-buy-calculator",
    "model-comparison-arena",
    # Section 2
    "classical-ml-playground",
    "metrics-explainer",
    "data-drift-simulator",
    "llm-vs-ml-showdown",
    # Section 3
    "token-counter",
    "temperature-playground",
    "prompt-engineering-lab",
    "prompt-injection-sim",
    "embedding-explorer",
    # Section 4
    "rag-playground",
    "rag-failure-simulator",
    "chunking-visualizer",
    "rag-vs-finetuning",
    "vector-db-cost-calculator",
    # Section 5
    "agent-workflow-builder",
    "agent-failure-gallery",
    "human-in-the-loop-designer",
    "tool-use-sandbox",
]


def deploy(apps_to_deploy=None):
    api = HfApi()

    # Get username
    try:
        username = api.whoami()["name"]
        print(f"Logged in as: {username}")
    except Exception:
        print("ERROR: Not logged in. Run: huggingface-cli login")
        sys.exit(1)

    # Find hf_spaces folder
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    hf_spaces_dir = repo_root / "hf_spaces"

    if not hf_spaces_dir.exists():
        print(f"ERROR: hf_spaces folder not found at {hf_spaces_dir}")
        sys.exit(1)

    # Use all apps or specific ones
    apps = apps_to_deploy if apps_to_deploy else APPS
    print(f"\nDeploying {len(apps)} app(s) from {hf_spaces_dir}\n")

    success = []
    failed = []

    for app in apps:
        space_id = f"{username}/{app}"
        local_path = hf_spaces_dir / app

        if not local_path.exists():
            print(f"SKIP: {app} - folder not found at {local_path}")
            failed.append((app, "folder not found"))
            continue

        try:
            # Create space if it doesn't exist
            create_repo(
                repo_id=space_id,
                repo_type="space",
                space_sdk="gradio",
                exist_ok=True
            )
            print(f"[+] Created/exists: {space_id}")

            # Upload all files
            upload_folder(
                folder_path=str(local_path),
                repo_id=space_id,
                repo_type="space"
            )
            url = f"https://huggingface.co/spaces/{space_id}"
            print(f"    Deployed: {url}")
            success.append((app, url))

        except Exception as e:
            print(f"[-] ERROR {app}: {e}")
            failed.append((app, str(e)))

    # Summary
    print("\n" + "=" * 50)
    print("DEPLOYMENT SUMMARY")
    print("=" * 50)
    print(f"\nSuccess: {len(success)}/{len(apps)}")
    for app, url in success:
        print(f"  - {app}: {url}")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for app, error in failed:
            print(f"  - {app}: {error}")

    print("\nDone!")
    return len(failed) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Gradio apps to HuggingFace Spaces")
    parser.add_argument("apps", nargs="*", help="Specific app(s) to deploy (default: all)")
    parser.add_argument("--list", action="store_true", help="List all available apps")
    args = parser.parse_args()

    if args.list:
        print("Available apps:")
        for app in APPS:
            print(f"  - {app}")
        sys.exit(0)

    # Validate app names if provided
    if args.apps:
        invalid = [a for a in args.apps if a not in APPS]
        if invalid:
            print(f"ERROR: Unknown app(s): {invalid}")
            print(f"Use --list to see available apps")
            sys.exit(1)

    success = deploy(args.apps if args.apps else None)
    sys.exit(0 if success else 1)
