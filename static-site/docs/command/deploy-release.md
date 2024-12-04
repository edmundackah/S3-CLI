# Deploy Release Build

## Description

The `deploy-release` command downloads a `.tgz` file from a specified URL (Artifactory), validates a change record with ServiceNow and uploads the contents of the `package/build` directory to an S3 bucket.

!!! warning "Mandatory Change Record"
    A valid change record is required to run this command.

## Usage

```sh
s3-cli deploy-release --url <URL> --bucket-name <BucketName> --prefix <Prefix> --change-record <ChangeRecord>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--url`: The URL of the `.tgz` file to download.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket-name`: The name of the S3 bucket.

- `--prefix`: The prefix to use for the S3 object keys (homepage path).

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-snapshot --bucket-name cli-demo --folder-path /Users/edmund/Documents/GitHub/SPA-Poc-CLI/src/test/resources/snapshot-test --prefix doc-test

2024-12-03 08:35:50,160 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 08:35:50,208 [INFO] Listing objects with prefix 'doc-test' in bucket 'cli-demo'...
2024-12-03 08:35:50,214 [WARNING] No objects found with prefix 'doc-test' in bucket 'cli-demo'.
2024-12-03 08:35:50,214 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 08:35:50,225 [INFO] Uploading /Users/edmund/Documents/GitHub/SPA-Poc-CLI/src/test/resources/snapshot-test/outer.txt to S3://cli-demo/doc-test/outer.txt with Content-Type: text/plain
2024-12-03 08:35:50,230 [INFO] Uploaded /Users/edmund/Documents/GitHub/SPA-Poc-CLI/src/test/resources/snapshot-test/outer.txt successfully.
2024-12-03 08:35:50,236 [INFO] Uploading /Users/edmund/Documents/GitHub/SPA-Poc-CLI/src/test/resources/snapshot-test/snapshot/inner.txt to S3://cli-demo/doc-test/snapshot/inner.txt with Content-Type: text/plain
2024-12-03 08:35:50,241 [INFO] Uploaded /Users/edmund/Documents/GitHub/SPA-Poc-CLI/src/test/resources/snapshot-test/snapshot/inner.txt successfully.
2024-12-03 08:35:50,241 [INFO] All files uploaded successfully.
```
</div>
