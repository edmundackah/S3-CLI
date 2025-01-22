# Remove Objects

## Description

The `remove-objects` deletes all objects from the bucket with object keys that match a given prefix.

!!! danger 
    This operation cannot be undone, take care when removing objects in production buckets.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when removing objects in a production S3 bucket.

```sh
s3-cli remove-objects --bucket <BucketName> --prefix <Prefix> --change-record <ChangeRecord> --target-server <TargetServer>
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
$ s3-cli remove-objects --bucket dev --prefix /snapshot

2024-12-03 12:47:42,273 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 12:47:42,325 [INFO] Listing objects with prefix 'snapshot' in bucket 'dev'...
2024-12-03 12:47:42,334 [INFO] Found 15 objects to delete.
2024-12-03 12:47:42,342 [INFO] Successfully deleted 15 objects.
```
</div>
