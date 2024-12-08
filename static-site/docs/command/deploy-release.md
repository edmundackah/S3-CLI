# Deploy Release Build

## Description

The `deploy-release` command downloads a `.tgz` file from a specified URL (Artifactory), 
validates a change record with ServiceNow and uploads the contents of the `package/build` directory to an S3 bucket.

!!! warning "Mandatory Change Record"
    A valid change record is required to run this command against a production bucket.

## Usage

```sh
s3-cli deploy-release --application <Application> --version <Version> --bucket-name <BucketName> --prefix <Prefix> --change-record <ChangeRecord>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--application`: The name of the application.

- `--version`: Application version number.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket-name`: The name of the S3 bucket.

- `--prefix`: The prefix to use for the S3 object keys (homepage path).

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-release --application test-app --version 1.0.0-aws --bucket-name prod --prefix release-test --change-record INC000000 --target-server AWS_S3

2024-12-05 20:52:37,110 [INFO] CLI running with profile: default
Validating change record: INC000000
2024-12-05 20:52:37,142 [INFO] Downloading release package from http://127.0.0.1:5000/download/tgz...
2024-12-05 20:52:37,143 [INFO] Downloaded tgz successfully.
2024-12-05 20:52:37,143 [INFO] Extracting tgz...
2024-12-05 20:52:37,146 [INFO] Extracted contents to release_extract.
2024-12-05 20:52:37,146 [INFO] Connecting to S3 Server: ECS_S3
2024-12-05 20:52:37,146 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-05 20:52:37,187 [INFO] Listing objects with prefix 'release-test' in bucket 'prod'...
2024-12-05 20:52:37,193 [WARNING] No objects found with prefix 'release-test' in bucket 'prod'.
2024-12-05 20:52:37,193 [INFO] Uploading contents of release_extract/package/build to bucket prod with prefix release-test...
2024-12-05 20:52:37,193 [INFO] Connecting to S3 Server: ECS_S3
2024-12-05 20:52:37,193 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-05 20:52:37,196 [INFO] Uploading release_extract/package/build/credentials 2.json to S3://prod/release-test/credentials 2.json with Content-Type: application/json
2024-12-05 20:52:37,202 [INFO] Uploaded release_extract/package/build/credentials 2.json successfully.
2024-12-05 20:52:37,202 [INFO] Uploaded release_extract/package/build to S3://prod/release-test/credentials 2.json.
2024-12-05 20:52:37,203 [INFO] Uploading release_extract/package/build/maintenance.json to S3://prod/release-test/maintenance.json with Content-Type: application/json
2024-12-05 20:52:37,207 [INFO] Uploaded release_extract/package/build/maintenance.json successfully.
2024-12-05 20:52:37,207 [INFO] Uploaded release_extract/package/build to S3://prod/release-test/maintenance.json.
2024-12-05 20:52:37,215 [INFO] Release package deployed successfully.
2024-12-05 20:52:37,215 [INFO] Cleaning up temporary files...
2024-12-05 20:52:37,215 [INFO] Removed tgz.
2024-12-05 20:52:37,216 [INFO] Removed release_extract.
2024-12-05 20:52:37,216 [INFO] Deployment completed successfully.
```
</div>
