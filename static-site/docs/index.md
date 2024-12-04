
# S3 Deployment CLI

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

A powerful command-line tool designed to automate **web applications deployment** and **streamline static files management**.

!!! tip "Get Started Quickly"
    Use the `--help` flag with any command to get detailed information about its usage:
    ```bash
    python s3-cli.py <command> --help
    ```
---
## 📦 Features

- **Snapshot Deployment**: Deploy snapshots to S3 buckets with ease.
- **Release Deployment**: Deploy releases directly from Artifactory `.tgz` files.
- **Maintenance Management**: Create, update, and verify maintenance flags in S3 buckets.
- **Object Verification**: List objects in S3 buckets and view metadata in an easy-to-read table.
- **Object Removal**: Remove objects from S3 buckets based on prefixes.

!!! info "Fully Integrated"
    S3 CLI integrates seamlessly with AWS S3 and ECS S3 environments.

---

## 🔧 Installation

Follow these steps to set up S3 CLI:

!!! note
    Python 3.9 or newer is required to run the CLI.

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/spa-cli.git
   ```

2. Navigate to the CLI directory:
   ```bash
   cd spa-cli
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your AWS credentials:
!!! danger
    It is best practice to configure S3 credentials using the AWS CLI. Click [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to read more.

   ```bash
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret-key
   ```

---

## 📖 Learn More

- For detailed command documentation, visit the [Commands](command/deploy-snapshot.md) section.
- Use the `--help` flag with any command to view detailed usage information:
  ```bash
  python cli.py <command> --help
  ```
