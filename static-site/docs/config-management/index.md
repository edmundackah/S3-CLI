# Configuration Management

This section explains how to configure and manage application profiles.
Profiles are defined in a YAML configuration file located at `resources/config.yaml`.
Profiles allow you to customise application settings based on the environment (e.g., `default`, `development`, `production`).

## Profile Structure

Each profile in the configuration file is defined as a key under the root object (e.g., `default`).
Here is an example of the `default` profile:

```yaml
profiles:
  default:
    prod_buckets: "prod,prd,prod-bucket"
    snow_broker:
      hostname: http://localhost:8080
      endpoint:
        incident: /incident
        change_record: /change/HBO%20Change
    ecs_s3:
      endpoint_url: http://localhost:9000
      region: us-east-1
      access_key_var: s3_local_aws_access_key_id
      secret_key_var: s3_local_aws_secret_access_key
```

!!! info
    AWS S3 Credentials is not configured in the configuration file and should be initialised using the AWS CLI to assume a role.

| **Property**                   | **Description**                                                                                        |
|--------------------------------|--------------------------------------------------------------------------------------------------------|
| `prod_buckets`                 | A comma-separated list of bucket names used for production. Automatically converted to a list in code. |
| `snow_broker.hostname`         | The base URL for the ServiceNow broker.                                                                |
| `snow_broker.endpoint.incident`| Path for incident-related operations.                                                                  |
| `snow_broker.endpoint.change_record` | Path for change record operations.                                                                     |
| `ecs_s3.endpoint_url`          | The base URL for the ECS S3 service.                                                                   |
| `ecs_s3.region`                | The default region for the ECS S3 service.                                                             |
| `ecs_s3.access_key_var`        | Name of the environment variable that stores the  ECS S3 access key.                                   |
| `ecs_s3.secret_key_var`        | Name of the environment variable that stores the ECS S3 secret key.                                    |


## Best Practices

!!! tip "Use Descriptive Profile Names"
    Examples: `default`, `development`, `production`. Avoid ambiguous names like `test` or `misc`.

!!! warning "Secure Environment Variables"
    Sensitive keys like `access_key_var` and `secret_key_var` should never be hardcoded in the YAML file or shared publicly.

!!! note "Document Profile-Specific Behavior"
    Add comments in `resources/config.yaml` to explain the purpose of each property, especially for profile-specific configurations.

