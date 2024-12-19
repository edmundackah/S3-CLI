# Deploy Local Build

## Description

The `deploy-snapshot` command validates a local folder and uploads its contents to an S3 bucket.

!!! warning
    The deploy snapshot command cannot deploy to production S3 buckets.

## Usage

```sh
s3-cli deploy-snapshot --folder-path <FolderPath> --bucket-name <BucketName> --prefix <Prefix> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--folder-path`: The path to the local folder to be uploaded.

- `--bucket-name`: The name of the S3 bucket.

- `--prefix`: The prefix to use for the S3 object keys (homepage path).

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-snapshot --bucket-name cli-demo --folder-path /snapshot-test --prefix /doc-test

2024-12-03 08:35:50,160 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 08:35:50,208 [INFO] Listing objects with prefix 'doc-test' in bucket 'cli-demo'...
2024-12-03 08:35:50,214 [WARNING] No objects found with prefix 'doc-test' in bucket 'cli-demo'.
2024-12-03 08:35:50,214 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 08:35:50,225 [INFO] Uploading /snapshot-test/outer.txt to S3://cli-demo/doc-test/outer.txt with Content-Type: text/plain
2024-12-03 08:35:50,230 [INFO] Uploaded /snapshot-test/outer.txt successfully.
2024-12-03 08:35:50,236 [INFO] Uploading /snapshot-test/snapshot/inner.txt to S3://cli-demo/doc-test/snapshot/inner.txt with Content-Type: text/plain
2024-12-03 08:35:50,241 [INFO] Uploaded /snapshot-test/snapshot/inner.txt successfully.
2024-12-03 08:35:50,241 [INFO] All files uploaded successfully.
```
</div>
