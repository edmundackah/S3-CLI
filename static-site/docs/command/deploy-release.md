# Deploy Release Build

## Description

The `deploy-release` command downloads a `.tgz` file from a specified URL (Artifactory), 
validates a change record with ServiceNow and uploads the contents of the `package/build` directory to an S3 bucket.

!!! warning "Mandatory Change Record"
    A valid change record is required to run this command against a production bucket.

!!! info "Metadata Support in Uploads"
    This command supports **S3 object metadata** using `-metadata.json` files.  
    If a file has a matching **`<filename>-metadata.json`**, its contents are used as metadata  
    and automatically prefixed with `x-amz-meta-`. The metadata JSON itself **is not uploaded**.  
    [Learn more →](./object-metadata.md)

## Usage

```sh
s3-cli deploy-release --application <Application> --version <Version> --bucket <BucketName> --prefix <Prefix> --change-record <ChangeRecord>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--application`: The name of the application.

- `--version`: Application version number.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket`: The name of the S3 bucket.

- `--prefix`: The prefix to use for the S3 object keys (homepage path).

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-release --application test-app --version 1.0.0 --bucket prod --prefix /release-test --change-record INC000000 --target-server ECS_S3
2024-12-08 12:38:05,266 [INFO] CLI running with profile: default
Validating change record: INC000000

2024-12-08 12:38:05,319 [INFO] Downloading release package from http://127.0.0.1:5000/artifactory/test-app/-/1.0.0/test-app-1.0.0.tgz...
2024-12-08 12:38:05,326 [INFO] Downloaded test-app-1.0.0.tgz successfully.
2024-12-08 12:38:05,326 [INFO] Extracting test-app-1.0.0.tgz...
2024-12-08 12:38:05,338 [INFO] Extracted contents to release_extract.
2024-12-08 12:38:05,338 [INFO] Connecting to S3 Server: ECS_S3
2024-12-08 12:38:05,338 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-08 12:38:05,398 [INFO] Listing objects with prefix 'release-test' in bucket 'prod'...
2024-12-08 12:38:05,405 [INFO] Found 4 objects to delete.
2024-12-08 12:38:05,408 [INFO] Successfully deleted 4 objects.
2024-12-08 12:38:05,408 [INFO] Uploading contents of release_extract/package/build to bucket prod with prefix release-test...
2024-12-08 12:38:05,408 [INFO] Connecting to S3 Server: ECS_S3
2024-12-08 12:38:05,408 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-08 12:38:05,412 [INFO] Uploading release_extract/package/build/preview.png to S3://prod/release-test/preview.png with Content-Type: image/png
2024-12-08 12:38:05,428 [INFO] Uploaded release_extract/package/build/preview.png successfully.
2024-12-08 12:38:05,428 [INFO] Uploaded release_extract/package/build to S3://prod/release-test/preview.png.

....

2024-12-08 12:38:05,468 [INFO] Release package deployed successfully.
2024-12-08 12:38:05,468 [INFO] Cleaning up temporary files...
2024-12-08 12:38:05,468 [INFO] Removed test-app-1.0.0.tgz.
2024-12-08 12:38:05,469 [INFO] Removed release_extract.
2024-12-08 12:38:05,469 [INFO] Deployment completed successfully.
```
</div>
