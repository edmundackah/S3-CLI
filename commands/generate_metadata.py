import os
from datetime import datetime, timezone

import typer

from utils.helpers import get_prod_buckets
from utils.util import write_json_file

app = typer.Typer()

def generate_metadata_file(folder_path: str, bucket_name: str, version: str):
    """
    Generates metadata files based on bucket type:
        - `BUILDINFO.json` for non-production buckets.
        - `VERSION.json` for production buckets (only contains project name & version).
        - If the bucket contains 'nft' and is non-production, generates **both** files.
    """

    # Retrieve GitLab CI environment variables
    project_name = os.getenv("CI_PROJECT_NAME", "unknown")

    is_production = any(bucket_name.lower() == b.lower() for b in get_prod_buckets())
    is_nft = "nft" in bucket_name.lower() and not is_production

    # Define metadata for BUILDINFO.json
    buildinfo_metadata = {
        "project_name": project_name,
        "version": version,
        "commit_hash": os.getenv("CI_COMMIT_SHA", "unknown"),
        "branch_name": os.getenv("CI_COMMIT_REF_NAME", "unknown"),
        "deployed_by": os.getenv("GITLAB_USER_LOGIN", "unknown"),  # Username of the person triggering the pipeline,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Define metadata for VERSION.json (only project name and version)
    version_metadata = {
        "project_name": project_name,
        "version": version
    }

    # Generate BUILDINFO.json for non-production or NFT buckets
    if not is_production or is_nft:
        buildinfo_path = os.path.join(folder_path, "BUILDINFO.json")
        write_json_file(buildinfo_path, buildinfo_metadata)

    # Generate VERSION.json for production or NFT buckets
    if is_production or is_nft:
        version_path = os.path.join(folder_path, "VERSION.json")
        write_json_file(version_path, version_metadata)