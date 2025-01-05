# Upload File To S3

## Description

The `upload-file` command will upload a specified file to an S3 bucket

!!! danger "Object Deletion"
    This command will overwrite existing objects in the target bucket. 
    You might want to enable object versioning on your bucket.

## Usage

!!! warning "Mandatory Change Record"
    A valid change record is required when uploading files to a production S3 bucket.

```sh
s3-cli upload-file --bucket <BucketName> --file-path <FilePath> --change-record <ChangeRecord> --target-server <TargetServer>
```

## Arguments

!!! info
    This command will connect to ECS S3 if a target server is not provided.

- `--bucket`: The name of the S3 bucket.

- `--file-path`:  Path to the file to upload.

- `--change-record`: The change record to validate with ServiceNow.

- `--target-server`: The target server to deploy to (e.g. AWS_S3 or ECS_S3)

## Example

<div class="termy">

```console
$ s3-cli upload-file --file-path "/Users/demo/test-file.txt" --bucket prod --change-record INC000000

2024-12-19 10:49:44,047 [INFO] CLI running with profile: default
Validating change record: INC000000

2024-12-19 10:49:44,099 [INFO] Starting file upload...
2024-12-19 10:49:44,099 [INFO] File Path: /Users/demo/test-file.txt
2024-12-19 10:49:44,099 [INFO] Bucket Name: prod
2024-12-19 10:49:44,099 [INFO] Connecting to S3 Server: ECS_S3
2024-12-19 10:49:44,099 [INFO] Accessing ECS_S3 endpoint: http://localhost:9000
2024-12-19 10:49:44,142 [INFO] Checking if object s3://prod/test-file.txt exists...
2024-12-19 10:49:44,148 [INFO] Object exists. Deleting it...
2024-12-19 10:49:44,152 [INFO] Object deleted successfully.
2024-12-19 10:49:44,152 [INFO] Uploading /Users/demo/test-file.txt to s3://prod/test-file.txt... with content-type: text/plain
File successfully uploaded to s3://prod/test-file.txt.
```
</div>
