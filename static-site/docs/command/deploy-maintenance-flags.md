# Deploy Maintenance Manifest

## Description
The `deploy-maintenance-flags` command is used to update the `maintenance.json` file stored in an S3 bucket.
This command takes the maintenance manifest yaml file as input and deploys only the changes.

!!! info 
    This command will create the maintenance file if the file doesn't exist in the specified bucket.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when interacting with a production S3 bucket.

```sh
s3-cli deploy-maintenance-flags --bucket <BucketName> --file <FilePath> --change-record <ChangeRecord> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--change-record`: The change record to validate with ServiceNow.

- `--bucket`: The name of the S3 bucket.

- `--file`: Desired state of the maintenance flags (e.g. true or false)

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli deploy-maintenance-flags --bucket dev --file maintenance-flags.yml

2024-12-26 15:31:47,067 [INFO] CLI running with profile: default
Starting maintenance flags update in bucket 'dev'...
Using maintenance file: maintenance-flags.yml
2024-12-26 15:31:47,126 [INFO] Connecting to S3 Server: ECS_S3
Fetching existing 'maintenance.json' from bucket...
Applying the following changes:
 - xo: false -> true
 - devops: None -> true
Uploading updated 'maintenance.json' to bucket...
Maintenance flags updated successfully.
```
</div>
