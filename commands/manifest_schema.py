import json
import yaml
import typer
from jsonschema import Draft7Validator

def validate_manifest(yaml_file: str):
    _validate_yaml(yaml_file, "resources/release-manifest-schema.json")


def validate_maintenance_yaml(yaml_file: str):
    _validate_yaml(yaml_file, "resources/maintenance-flag-schema.json")


def _validate_yaml(yaml_file: str, schema: str):
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as yf:
            yaml_data = yaml.safe_load(yf)

        # Load the JSON schema
        with open(schema, 'r') as sf:
            json_schema = json.load(sf)

        validator = Draft7Validator(json_schema)
        errors = list(validator.iter_errors(yaml_data))

        # Check for validation errors
        if errors:
            typer.echo("Validation failed! Errors found:", err=True)
            for error in errors:
                typer.echo(f"    - {'.'.join(map(str, error.absolute_path))}: {error.message}", err=True)
            raise typer.Exit(code=1)

        typer.echo("Validation successful! The YAML file is valid. 🥳")
    except FileNotFoundError as fnfe:
        typer.echo(f"File not found: {fnfe.filename}", err=True)
        raise typer.Exit(code=1)
    except yaml.YAMLError as ye:
        typer.echo(f"Failed to parse YAML: {ye}", err=True)
        raise typer.Exit(code=1)
    except json.JSONDecodeError as je:
        typer.echo(f"Failed to parse JSON schema: {je}", err=True)
        raise typer.Exit(code=1)