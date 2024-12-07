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
$ TBD
```
</div>
