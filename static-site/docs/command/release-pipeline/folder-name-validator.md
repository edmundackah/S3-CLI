# Validate Team Folder Names

## Description

The `validate-folder-names` command is used by the release pipeline to validates folder names 
in a given path against GitLab subgroups and nested subgroups. 
It ensures that each folder name matches a valid subgroup name in GitLab.

!!! warning "GitLab Access Token Required"
    GitLab token with `api` and `read_repository` privileges and a minimum of a developer role is required to use this command

## Usage

```sh
s3-cli validate-folder-names --file-path <FilePath> --subgroup-id <SubgroupID> --gitlab-url <GitlabUrl> --gitlab-token <Token>
```

## Arguments

!!! danger "Secrets Management"
    It is best practice to mount your gitlab token as environment variable, so it is not stored in your shell history.

- `--subgroup-id`: Top level GitLab subgroup ID to validate against.

- `--gitlab-url`: The name of the S3 bucket.

- `--gitlab-token`: The prefix to use for the S3 object keys (homepage path).

- `--file-path`: Path to validate folder names.

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
