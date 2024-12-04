# Toggle Maintenance Flags

## Description
The `deploy-maintenance` command is used to update the `maintenance.json` file stored in an S3 bucket. This command allows you to set the state (`true` or `false`) of specific maintenance flags.

!!! info 
    This command will create the maintenance flags if it doesn't already exist. It will also create the
    maintenance file, if the file doesn't exist in the specified bucket.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when interacting with a production S3 bucket.

```sh
s3-cli deploy-maintenance --bucket-name <BucketName> --flags <Flags> --state <State> --change-record <ChangeRecord> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket-name`: The name of the S3 bucket.

- `--state`: Desired state of the maintenance flags (e.g. true or false)

- `--flags`: Comma-separated list of flags to deploy.

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-maintenance --bucket-name dev --flags devops:test,xo,test2 --state true

2024-12-03 14:11:22,127 [INFO] Connecting to S3 Server: ECS_S3
2024-12-03 14:11:22,175 [INFO] Fetching maintenance.json from bucket dev...
2024-12-03 14:11:22,180 [WARNING] maintenance.json does not exist. Creating a new file.
2024-12-03 14:11:22,180 [INFO] Setting flag 'devops:test' to state 'true'.
2024-12-03 14:11:22,180 [INFO] Setting flag 'xo' to state 'true'.
2024-12-03 14:11:22,180 [INFO] Setting flag 'test2' to state 'true'.
2024-12-03 14:11:22,180 [INFO] Uploading updated maintenance.json to bucket dev...
2024-12-03 14:11:22,184 [INFO] Maintenance flags deployed successfully.
```
</div>
