# Creating a New Profile

To create a new profile, follow these steps:

Add the Profile to `resources/config.yaml`. Define a new profile under the root object. For example:

```yaml
development:
  prod_buckets: "prod-test-bucket"
  snow_broker:
    hostname: http://dev-server:8080
    endpoint:
      incident: /dev/incident
      change_record: /dev/change/HBO%20Change
  ecs_s3:
    endpoint_url: http://localhost:9000
    region: us-west-2
    access_key_var: dev_aws_access_key_id
    secret_key_var: dev_aws_secret_access_key
```

Set the `ACTIVE_PROFILE` variable to the new profile name:

```bash
export ACTIVE_PROFILE=development
```

Run the application and check that it is using the new profile's settings.

!!! important
    Ensure all required properties (e.g., `access_key_var`, `secret_key_var`) are correctly set in the new profile.
