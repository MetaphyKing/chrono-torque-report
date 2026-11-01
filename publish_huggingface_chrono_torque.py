#!/usr/bin/env python3
"""
publish_huggingface_chrono_torque.py
====================================
Creates and uploads the public `MetaphyKing/chrono-torque-report` repository on HuggingFace Hub.
"""
import pathlib
from huggingface_hub import HfApi

HERE = pathlib.Path(__file__).resolve().parent


def main():
    api = HfApi()
    repo_id = "MetaphyKing/chrono-torque-report"
    print(f"Creating/verifying HuggingFace repository: {repo_id}...")
    url = api.create_repo(repo_id=repo_id, repo_type="model", private=False, exist_ok=True)
    print(f"Repo URL: {url}")

    print("Uploading folder C:\\dev\\chrono-torque-report to HuggingFace Hub...")
    commit_info = api.upload_folder(
        folder_path=str(HERE),
        repo_id=repo_id,
        repo_type="model",
        ignore_patterns=[".git", ".git/*", ".vercel", ".vercel/*", "__pycache__", "__pycache__/*", "*.pyc"],
        commit_message="Release CHRONO-TORQUE (/gto v2.0 — UM-CGT-CLCOA v2.0) Triple-Verified Scientific Suite & 80-Kernel Arena",
    )
    print(f"[SUCCESS] Uploaded to HuggingFace Hub: {commit_info.commit_url}")


if __name__ == "__main__":
    main()
