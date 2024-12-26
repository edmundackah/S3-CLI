# Release Notes

---

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
