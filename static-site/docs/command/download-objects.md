# Download Objects

## Description

The `download-objects` command to download all files (or files matching a prefix) from an S3 bucket and package them into a ZIP file.  
  The ZIP file is named using the format `[bucket-name]-[target-server]-[timestamp].zip` and retains the original S3 object hierarchy.

!!! warning "Mandatory Change Record"
    A valid change record is required to run this command against a production bucket.

## Usage

```sh
s3-cli download-objects --bucket <BucketName> --prefix <Prefix> --change-record <ChangeRecord>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket`: The name of the S3 bucket.

- `--prefix`: Optional prefix to filter objects.

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli download-objects --bucket sit --prefix snapshots-test/api --target-server ECS_S3

2025-04-22 10:25:20,334 [INFO] CLI running with profile: dev
2025-04-22 10:25:20,382 [INFO] Connecting to S3 Server: ECS_S3
2025-04-22 10:25:20,382 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
Fetching object list from bucket 'sit'...
2025-04-22 10:25:20,438 [INFO] Skipping checksum validation. Response did not contain one of the following algorithms: ['crc32', 'sha1', 'sha256'].
2025-04-22 10:25:20,438 [INFO] Downloaded object: snapshots-test/api/axios.ts
2025-04-22 10:25:20,442 [INFO] Skipping checksum validation. Response did not contain one of the following algorithms: ['crc32', 'sha1', 'sha256'].
2025-04-22 10:25:20,443 [INFO] Downloaded object: snapshots-test/api/getDependencyTree.ts
ZIP file created: sit-ECS_S3-20250422-102520.zip
```
</div>
