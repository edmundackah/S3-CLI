# Switching Profiles

The active profile is determined by the environment variable `ACTIVE_PROFILE`. By default, the `default` profile is used if `ACTIVE_PROFILE` is not set.

## Switching Profiles

Set the `ACTIVE_PROFILE` Environment Variable**:
```bash
export ACTIVE_PROFILE=development
```

Run the Application

<div class="termy">

```console
$ python s3-cli.py --version

2024-12-04 14:10:02,304 [INFO] CLI running with profile: development
S3 CLI Version: 1.0.0
```
</div>

The application will use the settings defined under the `development` profile in `resources/config.yaml`.

!!! tip
    Always verify that the `ACTIVE_PROFILE` environment variable is correctly set before running the application.