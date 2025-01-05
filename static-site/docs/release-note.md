# Release Notes

---

## V3.0.0

!!! danger "💥 Breaking changes"
    - **Removed `validate-deployment-manifest` Command**: The `validate-deployment-manifest` command has been removed. Users relying on this command should migrate to alternative validation methods.
    
    - **Removed `validate-maintenance-flags` Command**: The `validate-maintenance-flags` command has been removed. Ensure to adapt workflows to the updated CLI.
    
    - **Renamed CLI Argument**: The `bucket-name` argument in the CLI has been renamed to `bucket`. Update scripts and workflows to use the new argument name.


### 🚀 New features (2)

- **Configuration Overrides**: Added the ability to override CLI configuration using environment variables. This feature allows dynamic customization of configuration values without modifying the YAML file.

- **Python 3.13 Compatibility**: Updated dependencies and ensured full compatibility with Python 3.13.

---

### 🔬 Improvements (1)
- **Argument Naming Update**: Renamed the `bucket-name` argument in the CLI to `bucket` for consistency and clarity.

---

### 📄 Documentation updates (2)
- **Removed Deployment Manifest Page**: The deployment manifest page has been removed from the documentation to align with the removal of the `validate-deployment-manifest` command.

- **Added Configuration Overrides Documentation**: Added a new page explaining the ability to override configuration using environment variables, including examples and best practices.

---

### 🧰 Maintenance (1)
- **Dependency Updates**: Updated CLI dependencies to ensure compatibility with the latest Python version (3.13) and maintain ecosystem stability.

---

### Additional Notes
- This release introduces breaking changes. Users are advised to review the release notes carefully and test their workflows before upgrading to ensure compatibility.

## V2.3.0

### 🚀 New features (1 change)
- Introduced the `deploy-maintenance-flags` command,
this command takes the maintenance manifest yaml file as input and deploys only the changes.

### 📄 Documentation updates (1 new page)
- **Deploy Maintenance Manifest**: Created a page to document the command

---

## V2.2.0

### 🚀 New features (1 change)
- Introduced the `upload-file` command, allowing users to upload files to S3 buckets.

!!! danger "Object Deletion"
    This command will overwrite existing objects in the target bucket. 
    You might want to enable object versioning on your bucket.

### 📄 Documentation updates (1 new page)
- **Upload File Command**: Created a page to document the upload file command

---

## V2.1.0

### 🔬 Improvements (1 change)
!!! danger "💥 Breaking changes"
    - Updated the `prefix` argument to require prefixes starting with a `/` for better consistency and usability.


### 🚀 New features (1 change)
!!! tip "Default Server"
    Defaults to ECS_S3 to preserve backwards compatibility with existing commands

- Added support for both **AWS S3** and **ECS S3** as target servers, enabling more flexibility in cloud environments.

---

## V2.0.0

!!! danger "💥 Breaking changes"
    - Ported the CLI to Python, introducing a complete overhaul of the CLI and breaking compatibility with the previous version.
    - Redesigned the API for improved modularity, maintainability, and extensibility. Existing workflows may require updates.

### 📄 Documentation updates (10+ pages)
- **S3 CLI Static Site**: Introduced static site to host the CLI documentation

### 🚀 New features (6 changes)
- **Deploy Snapshot**: Upload snapshot directories to S3 buckets.
- **Deploy Release**: Support `.tgz` packages for deployments from Artifactory to S3.
- **Deploy Maintenance**: Manage and deploy maintenance flags to S3.
- **Verify Maintenance**: Display the state of maintenance flags in a table.
- **Remove Objects**: Delete objects from S3 buckets based on prefixes.
- **Verify**: List and display metadata of objects in S3 buckets.
- **Change Record Validation**: Added command to view MCRs and INCs
