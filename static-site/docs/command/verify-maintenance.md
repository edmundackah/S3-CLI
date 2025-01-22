# View Maintenance Flags

## Description
The `verify-maintenance` command is used to verify the states of all flags in the `maintenance.json` file stored in an S3 bucket. 
It displays the results in a table format.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when interacting with a production S3 bucket.

```sh
s3-cli verify-maintenance --bucket <BucketName> --change-record <ChangeRecord> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket`: The name of the S3 bucket.

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli verify-maintenance --bucket dev

2024-12-03 14:47:20,406 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 14:47:20,454 [INFO] Fetching maintenance.json from bucket dev...
+-------------+---------+
| Flag        | State   |
+=============+=========+
| devops:test | false   |
+-------------+---------+
| xo          | false   |
+-------------+---------+
| test2       | false   |
+-------------+---------+
```
</div>
