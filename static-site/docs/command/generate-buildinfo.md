# Generate Build Metadata

## Description
The `generate-metadata` command is used create the metadata json files containing information about the objects deployed to S3.

!!! info 
    This command creates a `BUILDINFO.json` file when a non-prod bucket is provided and a `VERSION.json` for prod buckets. 
    If a bucket name containing the phrase `nft` is provided, then both files are generated.

## Usage

```sh
s3-cli generate-metadata --bucket <BucketName> --folder-path <FolderPath> --version <Version>
```

## Arguments

- `--bucket`: The name of the S3 bucket.

- `--folder-path`: Path to the folder where the file will be created.

- `--version`: The application version number.

## Example

<div class="termy">

```console
$ s3-cli generate-metadata --bucket nft --folder-path static-site --version 1.0.0

2025-02-08 19:07:30,923 [INFO] CLI running with profile: default
File 'static-site/BUILDINFO.json' created with contents:
        {'project_name': 'unknown', 'version': '1.0.0', 
        'commit_hash': 'unknown', 'branch_name': 'unknown', 
        'deployed_by': 'unknown', 
        'timestamp': '2025-02-08T19:07:30.971335+00:00'}

Overwritten: static-site/BUILDINFO.json
File 'static-site/VERSION.json' created with contents:
        {'project_name': 'unknown', 'version': '1.0.0'}

Overwritten: static-site/VERSION.json
```
</div>
