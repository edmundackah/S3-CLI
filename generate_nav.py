import os
import re
import sys
import yaml
import argparse

# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"

# Safe loader to ignore custom YAML tags
class IgnoreUnknownTagsLoader(yaml.SafeLoader):
    pass

def ignore_unknown_tags(loader, tag_suffix, node):
    """Custom constructor to ignore unknown YAML tags."""
    return None  # Ignore the tagged content

IgnoreUnknownTagsLoader.add_multi_constructor("tag:yaml.org,2002:", ignore_unknown_tags)

def get_first_header(filepath):
    """Extract the first header from a Markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                match = re.match(r"^(#{1,6})\s+(.+)", line)
                if match:
                    return match.group(2)  # Return the header text
    except Exception as e:
        print(f"{RED}ERROR: Failed to read {filepath}: {e}{RESET}")
    return None

def format_folder_name(folder_name):
    """Format folder names to preserve hyphen-separated parts."""
    return " ".join(part.capitalize() for part in folder_name.split('-'))

def generate_nav(directory, ignore_dirs):
    """Generate the nav structure based on directory contents, preserving numerical order."""
    print(f"{BLUE}DEBUG: Generating navigation structure for directory: {directory}{RESET}")
    nav = []
    home_section = {"Home": []}  # Root-level "Home" section
    home_page_set = False

    for root, dirs, files in os.walk(directory):
        # Ignore hidden files and directories specified in ignore_dirs
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Sort files and directories numerically if they start with numbers
        files.sort(key=lambda x: int(x.split('-')[0]) if x[0].isdigit() else x)
        dirs.sort(key=lambda x: int(x.split('-')[0]) if x[0].isdigit() else x)

        # Relative path to the root directory
        rel_path = os.path.relpath(root, directory)
        if rel_path == ".":
            rel_path = ""

        # Process root-level files (Home section)
        if rel_path == "":
            for file in files:
                filepath = os.path.join(root, file)

                # Handle root-level index.md as the main Home page
                if file == "index.md":
                    home_section["Home"].insert(0, {f"Home": f"{file}"})
                    home_page_set = True
                elif file.endswith(".md"):
                    # Add other root-level Markdown files to the Home section
                    header = get_first_header(filepath)
                    title = header if header else os.path.splitext(file)[0].capitalize()
                    home_section["Home"].append({title: f"{file}"})

        # Process subdirectories
        else:
            section = []
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    # Extract the first header if available
                    header = get_first_header(filepath)
                    title = header if header else os.path.splitext(file)[0].capitalize()
                    section.append({title: f"{rel_path}/{file}".lstrip('/')})

            # Add sections only if files exist
            if section:
                folder_name = format_folder_name(os.path.basename(rel_path))
                nav.append({folder_name: section})

    # Add Home section to the beginning of the nav
    if home_section["Home"]:
        nav.insert(0, home_section)

    if not home_page_set:
        print(f"{YELLOW}WARNING: No root index.md file found. Add one for a Home page.{RESET}")

    return nav

def update_mkdocs_config(docs_directory, config_file, ignore_dirs):
    """Update the mkdocs.yml with the generated nav."""
    if not os.path.exists(config_file):
        print(f"{RED}ERROR: Configuration file {config_file} not found.{RESET}")
        sys.exit(1)

    with open(config_file, "r") as f:
        # Use the custom loader to ignore unknown tags
        config = yaml.load(f, Loader=IgnoreUnknownTagsLoader)

    # Check if nav already exists
    if "nav" in config:
        print(f"{GREEN}INFO: Navigation is already defined in {config_file}. Exiting.{RESET}")
        sys.exit(0)

    print(f"{BLUE}DEBUG: Generating navigation for {docs_directory}, ignoring directories: {ignore_dirs}{RESET}")
    nav_structure = generate_nav(docs_directory, ignore_dirs)
    config["nav"] = nav_structure

    # Fix YAML formatting explicitly
    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, Dumper=yaml.Dumper, width=80, allow_unicode=True)

    print(f"{GREEN}INFO: Navigation has been successfully updated in {config_file}.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MkDocs navigation dynamically.")
    parser.add_argument(
        "--docs-dir", type=str, default="docs",
        help="Path to the directory containing Markdown files (default: docs/)."
    )
    parser.add_argument(
        "--config-file", type=str, default="mkdocs.yml",
        help="Path to the MkDocs YAML configuration file (default: mkdocs.yml)."
    )
    args = parser.parse_args()

    # Get ignore directories from environment variable
    ignore_dirs_env = os.getenv("IGNORE_DIRS", "")
    ignore_dirs = ignore_dirs_env.split(",") if ignore_dirs_env else []

    print(f"{BLUE}DEBUG: Starting MkDocs nav generation script.{RESET}")
    update_mkdocs_config(args.docs_dir, args.config_file, ignore_dirs)