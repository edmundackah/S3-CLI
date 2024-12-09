import os
import yaml
from jinja2 import Template


class PipelineGenerator:
    def __init__(self, template_file):
        self.template_file = template_file

    def read_file_paths(self, file_path):
        """Read file paths from a text file."""
        if not os.path.exists(file_path):
            print(f"INFO: '{file_path}' not found. Skipping.")
            return []
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def load_yaml(self, file_path):
        """Load a YAML file and return its content."""
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Skipping.")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file '{file_path}': {e}")
            return None

    def load_template(self):
        """Load the unified Jinja2 template."""
        with open(self.template_file, 'r') as file:
            return Template(file.read())

    def bucket_name_selector(self, env_name, target_server):
        """Generate bucket name based on environment and target server."""
        return f"{env_name}-bucket-{target_server.lower()}"

    def process_maintenance_files(self, maintenance_files):
        """Process maintenance YAML files and generate job contexts."""
        maintenance_jobs = []
        for file_path in maintenance_files:
            yaml_data = self.load_yaml(file_path)
            if not yaml_data:
                continue

            env_name = os.path.basename(os.path.dirname(file_path))
            is_aws = "-aws" in file_path
            off_flags = ",".join([flag["flag"] for flag in yaml_data.get("flags", []) if not flag["state"]])
            on_flags = ",".join([flag["flag"] for flag in yaml_data.get("flags", []) if flag["state"]])

            maintenance_jobs.append({
                "env": env_name,
                "target": "-aws" if is_aws else "",
                "target_server": "AWS_S3" if is_aws else "ECS_S3",
                "bucket_name": self.bucket_name_selector(env_name, "AWS_S3" if is_aws else "ECS_S3"),
                "change_record": yaml_data.get("changeRecord", "N/A"),
                "off_flags": off_flags or "N/A",
                "on_flags": on_flags or "N/A",
            })
        return maintenance_jobs

    def process_spa_files(self, spa_files):
        """Process SPA YAML files and generate job contexts for deploy and removal."""
        spa_jobs = []
        removal_jobs = []
        for file_path in spa_files:
            yaml_data = self.load_yaml(file_path)
            if not yaml_data:
                continue

            env_name = os.path.basename(os.path.dirname(file_path))
            for server in yaml_data.get("targetServer", []):
                target = "-aws" if server == "AWS_S3" else ""
                job_context = {
                    "application": yaml_data.get("projectName"),
                    "version": yaml_data.get("version"),
                    "target": target,
                    "target_server": server,
                    "bucket_name": self.bucket_name_selector(env_name, server),
                    "prefix": yaml_data.get("homepage").lower().lstrip("/"),
                    "change_record": yaml_data.get("changeRecord"),
                }
                if yaml_data.get("action") == "DEPLOY":
                    spa_jobs.append(job_context)
                elif yaml_data.get("action") == "REMOVE":
                    removal_jobs.append(job_context)
        return spa_jobs, removal_jobs

    def generate_pipeline(self, maintenance_files_path, spa_files_path, output_file_path):
        """Generate pipeline YAML by rendering the Jinja2 template."""
        # Read file paths
        maintenance_files = self.read_file_paths(maintenance_files_path)
        spa_files = self.read_file_paths(spa_files_path)

        # Process files to extract contexts
        maintenance_jobs = self.process_maintenance_files(maintenance_files)
        spa_jobs, removal_jobs = self.process_spa_files(spa_files)

        # Load the Jinja2 template
        template = self.load_template()

        # Determine whether to include "do nothing" jobs
        include_do_nothing_maintenance = len(maintenance_jobs) == 0
        include_do_nothing_spa = len(spa_jobs) == 0 and len(removal_jobs) == 0

        # Render the pipeline
        rendered_pipeline = template.render(
            maintenance_jobs=maintenance_jobs,
            spa_jobs=spa_jobs,
            removal_jobs=removal_jobs,
            include_do_nothing_maintenance=include_do_nothing_maintenance,
            include_do_nothing_spa=include_do_nothing_spa,
        )

        # Save the rendered pipeline to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(rendered_pipeline)
        print(f"Pipeline saved to {output_file_path}")


if __name__ == "__main__":
    # Configuration
    TEMPLATE_FILE = "ci/templates/pipeline_template.j2"
    MAINTENANCE_FILES_PATH = "modified_maintenance_files.txt"
    SPA_FILES_PATH = "spa-releases.txt"
    OUTPUT_FILE = "generated-pipeline.yml"

    # Generate the pipeline
    generator = PipelineGenerator(TEMPLATE_FILE)
    generator.generate_pipeline(MAINTENANCE_FILES_PATH, SPA_FILES_PATH, OUTPUT_FILE)