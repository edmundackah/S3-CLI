# Deployment manifest Schema

This page provides the JSON schema for validating deployment manifests and explains the constraints. 
Additionally, sample files for each supported deployment action (`DEPLOY`, `REMOVE`, and `MAINTENANCE`) are provided for reference.

## JSON Schema
The following JSON schema validates the deployment manifest:

??? abstract "Manifest JSON Schema"
    ```json
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "required": ["projectName", "technicalSme", "supportEmail", "action", "targetServer", "version", "changeRecord", "homepage"],
      "properties": {
        "projectName": {
          "type": "string",
          "minLength": 1,
          "description": "The name of the project (required)."
        },
        "technicalSme": {
          "type": "string",
          "minLength": 1,
          "description": "The name of the technical SME (required)."
        },
        "supportEmail": {
          "type": "string",
          "format": "email",
          "description": "The support email address (required)."
        },
        "action": {
          "type": "string",
          "enum": ["DEPLOY", "REMOVE"],
          "description": "The action to perform (required). Supported actions: DEPLOY, REMOVE."
        },
        "targetServer": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["ECS_S3", "AWS_S3"]
          },
          "minItems": 1,
          "description": "The target server(s) for deployment (required)."
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9\\-\\.]+)?(\\+[A-Za-z0-9\\-\\.]+)?$",
          "description": "The version of the deployment (required). Must follow semantic versioning, including optional pre-release and build metadata."
        },
        "changeRecord": {
          "type": "string",
          "minLength": 1,
          "description": "The change record associated with the deployment (required)."
        },
        "homepage": {
          "type": "string",
          "pattern": "^/[^/]+(/[^/]+)*$",
          "description": "The homepage path of the application (required). Must follow the format '/path/to/resource'."
        }
      }
    }
    ```

## Constraints and Validation Rules

!!! info
    - Fields marked as **Conditional** (like `maintenanceFlags`) depend on the value of other fields (e.g., `action`).
    - The `homepage` field is validated using a regular expression to ensure it follows the specified path format.

| **Field**            | **Required** | **Description**                                                                                       | **Validation Rules**                                                                 |
|----------------------|--------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| `projectName`        | Yes          | The name of the project.                                                                              | Must be a non-empty string.                                                          |
| `technicalSme`       | Yes          | The name of the technical SME.                                                                        | Must be a non-empty string.                                                          |
| `supportEmail`       | Yes          | The support email address.                                                                            | Must be a valid email address.                                                       |
| `action`             | Yes          | The action to perform.                                                                                | Must be one of `DEPLOY` or `REMOVE`.                                                 |
| `targetServer`       | Yes          | The target server(s) for deployment.                                                                  | Must include one or more values from `ECS_S3` or `AWS_S3`.                           |
| `version`            | Yes          | The version of the deployment.                                                                        | Must follow semantic versioning (e.g., `1.0.0` or `1.0.0-aws`).                      |
| `changeRecord`       | Yes          | The change record associated with the deployment.                                                     | Must be a non-empty string.                                                          |
| `homepage`           | Yes          | The homepage path of the application.                                                                 | Must follow the format `/path/to/resource`.                                          |

## Example Manifests
Here are some example deployment manifest. 
Please consult the table above to understand the constraints associated with the various deployment activities.

### Deployment manifest

```yaml
projectName: ui-spa-consent-to-let
technicalSme: John Doe
supportEmail: test@test.com
action: DEPLOY
targetServer:
  - ECS_S3
version: 1.0.0
changeRecord: MCR1000
homepage: /servicing/customer/consent-to-let
```

### Removal manifest

```yaml
projectName: ui-spa-consent-to-let
technicalSme: John Doe
supportEmail: test@test.com
action: REMOVE
targetServer:
  - AWS_S3
  - ECS_S3
version: 1.0.0
changeRecord: MCR1001
homepage: /servicing/customer/consent-to-let
```