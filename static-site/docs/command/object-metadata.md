# Adding S3 Object Metadata

## Overview
The `deploy-snapshot` and `deploy-release` command now supports **object metadata** using JSON metadata files.
If a file has an associated **`.meta.json`** file, its contents are used as metadata for the object when uploaded to S3.
The metadata JSON file itself is **not uploaded**.

!!! note "Metadata JSON Naming"
    The metadata file must be named **`<filename>.meta.json`** to be recognized.  
    Example:  
    - `index.html` → **`index.html.meta.json`**  
    - `style.css` → **`style.css.meta.json`**

## How It Works
1. The script scans the folder for files to upload.
2. If a `.meta.json` file exists, its contents are **read and used as metadata**.
3. **All metadata keys are prefixed with `x-amz-meta-`** (as per Amazon S3 specs).
4. The metadata file itself **is not uploaded**.

!!! example "Example Folder Structure"
    ```
    my-folder/
    ├── index.html
    ├── index.html.meta.json
    ├── script.js
    ├── styles.css
    ├── styles.css.meta.json
    ```

## Example Metadata File

```json
{
    "author": "john_doe",
    "content-type": "text/html",
    "custom-header": "my-value"
}
```

!!! warning "Automatic Metadata Key Formatting"
    If the keys in the metadata JSON **do not start with** `"x-amz-meta-"`,  
    the script **automatically adds the prefix**.

## Uploading with Metadata
Run the command as usual:

<div class="termy">

```console
$ s3-cli deploy-snapshot --bucket cli-demo --folder-path /snapshot-test --prefix /doc-test
```
</div>

!!! success "Files Uploaded"
    ✅ `index.html` (Uploaded with metadata)  
    ✅ `styles.css` (Uploaded with metadata)  
    ✅ `script.js` (Uploaded normally)  
    ❌ `index.html.meta.json` (Skipped)  
    ❌ `styles.css.meta.json` (Skipped)  

## Logging
When a metadata file is used, the CLI logs:

```plaintext
Using metadata from index.html.meta.json:
{'x-amz-meta-author': 'john_doe', 'x-amz-meta-content-type': 'text/html', 'x-amz-meta-custom-header': 'my-value'}
```

!!! tip "S3-Specific Metadata"
    The script ensures that metadata keys follow the **S3 metadata naming convention**  
    to prevent unexpected behavior when retrieving objects.