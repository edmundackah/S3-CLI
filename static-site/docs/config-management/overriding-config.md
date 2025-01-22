# Overriding CLI Configuration

The CLI application provides a flexible way to override configuration values defined in the YAML file using environment variables.
This is especially useful for managing different environments or deployments, when running the CLI as a compiled binary.

## Getting Started

All configuration overrides must use the prefix `S3_CLI_`. 
This ensures that only relevant environment variables are considered for overriding.

YAML keys are mapped to environment variable names using underscores (`_`) and double underscores (`__`) for nested keys.

!!! example
    - YAML key: `prod_buckets` → Environment Variable: `S3_CLI_PROD_BUCKETS`
    - Nested YAML key: `artifactory.spa_pattern` → Environment Variable: `S3_CLI_ARTIFACTORY__SPA_PATTERN`


## Usage Example

Assuming the CLI is running with the dev profile and the YAML configuration contains the snippet below.

```yaml
  dev:
    prod_buckets: "prod,prd,prod-bucket"
    artifactory:
      spa_pattern: "http://127.0.0.1:5000-a"
```

We can override the two properties by setting the environment variables below.

<div class="termy">

```console
// Override the 'prod_buckets' field
export S3_CLI_PROD_BUCKETS="custom_bucket_name"

// Override the 'artifactory.spa_pattern' field
export S3_CLI_ARTIFACTORY__SPA_PATTERN="http://custom_artifactory_url"

// Enable detailed logging of overrides
export S3_CLI_LOGGING=DEBUG
```

</div>

!!! warning "Environment Variables Take Precedence"
    If an environment variable is set for a configuration field, it will override the value from the YAML file.

## Logging Configuration

The CLI logs all detected environment variables used for overrides. The level of detail depends on the `S3_CLI_LOGGING` environment variable.
By default, only the names of detected environment variables are logged.

```plaintext
2025-01-05 12:34:56 [INFO] Detected override: S3_CLI_PROD_BUCKETS
2025-01-05 12:34:56 [INFO] Detected override: S3_CLI_ARTIFACTORY__SPA_PATTERN
```

When `S3_CLI_LOGGING=DEBUG` is set, both the names and values of the environment variables are logged.

!!! danger "Avoid Logging Sensitive Data"
    Be cautious about enabling `DEBUG` logging in production environments, as it may log sensitive configuration values.

```plaintext
2025-01-05 12:34:56 [INFO] Detected override: S3_CLI_PROD_BUCKETS -> prod_buckets = custom_bucket_name
2025-01-05 12:34:56 [INFO] Detected override: S3_CLI_ARTIFACTORY__SPA_PATTERN -> artifactory.spa_pattern = http://custom_artifactory_url
```
