from typing import Optional

import typer

from commands.change_record_overview import find_change_record
from commands.deploy_release import deploy_release
from commands.deploy_snapshot import deploy_snapshot
from commands.list_objects import list_objects
from commands.maintenance import verify_maintenance, deploy_maintenance
from commands.manifest_schema import validate_manifest, validate_maintenance_yaml
from commands.remove_objects import remove_objects
from utils.config_manager import ConfigManager
from utils.helpers import validate_prefix, validate_bucket_name, validate_change_record, TargetServer, validate_boolean

app = typer.Typer()

# Load the configuration at the start
config = ConfigManager.get_config()

@app.command("deploy-snapshot")
def deploy_snapshot_command(
    folder_path: str = typer.Option(..., "--folder-path", help="Path to the folder containing the snapshot"),
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket", callback=validate_bucket_name),
    prefix: str = typer.Option(..., "--prefix", help="Object key prefix", callback=validate_prefix),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server for deployment")
):
    """Deploy a snapshot to the specified target server."""
    deploy_snapshot(folder_path, bucket_name, prefix, target_server)


@app.command("deploy-release")
def deploy_release_command(
    url: str = typer.Option(..., "--url", help="Artifactory URL of the release to deploy"),
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket"),
    prefix: str = typer.Option(..., "--prefix", help="Object key prefix", callback=validate_prefix),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server for deployment"),
    change_record: Optional[str] = typer.Option(None,"--change-record",
                                                help="Change record required to authorise prod change",
                                                callback=validate_change_record)
):
    """Deploy a release to the specified target server."""
    deploy_release(url, bucket_name, prefix, target_server)


@app.command("remove-objects")
def remove_objects_command(
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket"),
    prefix: str = typer.Option(..., "--prefix", help="Object key prefix", callback=validate_prefix),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server for object removal"),
    change_record: Optional[str] = typer.Option(None,"--change-record",
                                                help="Change record required to authorise prod change",
                                                callback=validate_change_record)
):
    """Remove objects from a bucket with the given object key prefix."""
    remove_objects(bucket_name, prefix, target_server)


@app.command("verify-maintenance")
def verify_maintenance_command(
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket"),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server"),
    change_record: Optional[str] = typer.Option(None,"--change-record",
                                                help="Change record required to authorise prod change",
                                                callback=validate_change_record)
):
    """Verify the contents of the maintenance.json file in the specified bucket."""
    verify_maintenance(bucket_name, target_server)


@app.command("deploy-maintenance")
def deploy_maintenance_command(
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket"),
    flags: str = typer.Option(..., "--flags", help="Comma-separated list of flags to deploy"),
    state: str = typer.Option(..., "--state", help="State to set for the flags (e.g. true or false)", callback=validate_boolean),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server for deployment"),
    change_record: Optional[str] = typer.Option(None,"--change-record",
                                                help="Change record required to authorise prod change",
                                                callback=validate_change_record)
):
    """Deploy or update maintenance flags in the specified bucket."""
    deploy_maintenance(bucket_name, flags, state, target_server)


@app.command("list-objects")
def list_objects_command(
    bucket_name: str = typer.Option(..., "--bucket-name", help="Name of the S3 bucket"),
    prefix: str = typer.Option("", "--prefix", help="Prefix to filter objects in the bucket", callback=validate_prefix),
    target_server: TargetServer = typer.Option(TargetServer.ECS_S3, "--target-server", help="Target server for deployment"),
    change_record: Optional[str] = typer.Option(None,"--change-record",
                                                help="Change record required to authorise prod change",
                                                callback=validate_change_record)
):
    """List and display objects in an S3 bucket as a table."""
    list_objects(bucket_name, prefix, target_server)


@app.command("view-change-record")
def view_change_record(mcr_number: str = typer.Option(..., "--number", help="e.g. MCR00000 / INC00000")):
    """Pulls change record or incident details from ServieNow"""
    find_change_record(mcr_number)


@app.command("validate-manifest")
def validate_release_manifest(file_path: str = typer.Option(..., "--file", help="Path to the release manifest"),
        subgroup_id: int = typer.Option(..., "--subgroup-id", help="GitLab subgroup ID to validate against."),
        gitlab_url: str = typer.Option(..., "--gitlab-url", help="URL of the GitLab server."),
        gitlab_token: str = typer.Option(..., "--gitlab-token", help="Private access token for GitLab API.")
):
    """Validates a release manifest using the JSON Schema"""
    validate_manifest(file_path, subgroup_id, gitlab_url, gitlab_token)


@app.command("validate-maintenance-file")
def validate_maintenance_file(
        file_path: str = typer.Option(..., "--file", help="Path to the maintenance flags file"),
        subgroup_id: int = typer.Option(..., "--subgroup-id", help="GitLab subgroup ID to validate against."),
        gitlab_url: str = typer.Option(..., "--gitlab-url", help="URL of the GitLab server."),
        gitlab_token: str = typer.Option(..., "--gitlab-token", help="Private access token for GitLab API.")
):
    """Validates the maintenance flags yaml using the JSON Schema"""
    validate_maintenance_yaml(file_path, subgroup_id, gitlab_url, gitlab_token)


@app.command()
def version():
    typer.echo("S3 CLI Version: 1.0.0")


if __name__ == "__main__":
    app()