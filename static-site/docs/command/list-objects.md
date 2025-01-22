# List Objects

## Description

The `list-objects` command renders a table listing all objects in the specified bucket, if the object key
starts with the given prefix.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when listing objects in a production S3 bucket.

```sh
s3-cli list-objects --bucket <BucketName> --prefix <Prefix> --change-record <ChangeRecord> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket`: The name of the S3 bucket.

- `--prefix`: The prefix to use for the S3 object keys (homepage path).

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli list-objects --bucket cli-demo --prefix /doc-test

2024-12-05 20:33:47,636 [INFO] CLI running with profile: default
2024-12-05 20:33:47,663 [INFO] Connecting to S3 Server: ECS_S3
2024-12-05 20:33:47,663 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-05 20:33:47,704 [INFO] Listing objects in bucket 'cli-demo' with prefix 'doc-test'...
+-----------------------------+---------------------+----------------+
| Key                         | Date Modified       |   Size (Bytes) |
+=============================+=====================+================+
| doc-test/.DS_Store          | 04/12/2024 12:06:31 |           6148 |
+-----------------------------+---------------------+----------------+
| doc-test/outer - Copy.txt   | 04/12/2024 12:06:31 |             36 |
+-----------------------------+---------------------+----------------+
| doc-test/outer.txt          | 04/12/2024 12:06:31 |             36 |
+-----------------------------+---------------------+----------------+
| doc-test/snapshot/inner.txt | 04/12/2024 12:06:31 |             36 |
+-----------------------------+---------------------+----------------+
```
</div>
