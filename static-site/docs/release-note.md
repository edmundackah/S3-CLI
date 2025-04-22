# Release Notes

---

## V3.4.0

### 🚀 New features (1)

- **Download and Zip S3 Objects**:  
  Added a new `download-objects` command to download all files (or files matching a prefix) from an S3 bucket and package them into a ZIP file.  
  The ZIP file is named using the format `[bucket-name]-[target-server]-[timestamp].zip` and retains the original S3 object hierarchy.

### 📄 Documentation updates (1)

- **New Page: Download Objects**  
  A new documentation page has been added under the **Commands** section to explain  the `download-objects` command.


## V3.2.0

### 🧰 Maintenance (1)
- **Dependency Updates**: Updated CLI dependencies to address vulnerabilities.

### 🚀 New features (2)
- **Generate Metadata Command**: Added a new command for generating **BUILDINFO** and **VERSION** files.

- **Metadata Support for Upload Command**: The `deploy-snapshot` and `deploy-release` command now supports metadata JSON files.  
  If a file has an associated `<filename>.meta.json`, its contents are applied as **object metadata** during upload.  

!!! note "Automatic Metadata Key Formatting"
    If the keys in the metadata JSON **do not start with** `"x-amz-meta-"`,  
    the CLI **automatically adds the prefix** to comply with Amazon S3 specifications.

!!! example "Example Folder Structure"
    ```
    my-folder/
    ├── index.html
    ├── index.html.meta.json
    ├── script.js
    ├── styles.css
    ├── styles.css.meta.json
    ```
  
!!! success "Improved Upload Handling"
    - Metadata JSON files **are not uploaded** to S3.  
    - Objects are now uploaded **with correct metadata** based on their JSON metadata file.  
    - Logging improvements ensure **clear visibility** of applied metadata.

### 📄 Documentation updates (1)
- **New Page: Upload Command Metadata**  
  A new documentation page has been added under the **Commands** section to explain how metadata JSON files work with the `upload-folder` command.

---

## V3.1.0

### 🧰 Maintenance (1)
- **Updated application profiles**: Updated CLI profiles to remove mockdata in dev and prod profiles.

## V3.0.0

!!! danger "💥 Breaking changes"
    - **Removed `validate-folder-names` Command**: The `validate-folder-names` command has been removed. Ensure to adapt workflows to the updated CLI.
    
    - **Renamed CLI Argument**: The `bucket-name` argument in the CLI has been renamed to `bucket`. Update scripts and workflows to use the new argument name.

### 🚀 New features (2)

- **Configuration Overrides**: Added the ability to override CLI configuration using environment variables. This feature allows dynamic customization of configuration values without modifying the YAML file.

- **Python 3.13 Compatibility**: Updated dependencies and ensured full compatibility with Python 3.13.

---

### 🔬 Improvements (2)
- **Argument Naming Update**: Renamed the `bucket-name` argument in the CLI to `bucket` for consistency and clarity.

- **ANSI Colours**: Created a new logging util to address ANSI colours not appearing in GitLab CI Terminal.

---

### 📄 Documentation updates (1)
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