# Managing maintenance flags

This page provides details on how to toggle and manage the SPA maintenance flags.
The YAML file in each environment acts as a state file documenting the state of the environment.
Deploying a maintenance flag is as simple as updating an existing flag in the YAML or adding a new flag
if the flag is not present.

## JSON Schema
The following JSON schema validates the maintenance flag YAML:

??? abstract "Maintenance Flags JSON Schema"
    ```json
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "required": ["changeRecord", "flags"],
      "properties": {
        "changeRecord": {
          "type": "string"
        },
        "flags": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "object",
            "required": ["flag", "state", "description", "dependencies"],
            "properties": {
              "flag": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9:-]+$"
              },
              "state": {
                "type": "boolean"
              },
              "description": {
                "type": "string",
                "minLength": 20
              },
              "dependencies": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": true,
                "items": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
    ```

## Constraints and Validation Rules

| Field                 | Type        | Constraints                                                                |
|-----------------------|-------------|----------------------------------------------------------------------------|
| `changeRecord`        | `string`    | Required field.                                                            |
| `flags`               | `array`     | Required field. All items must be unique.                                  |
| `flags[].flag`        | `string`    | Required field. Can contain alphanumeric characters, `:`, and `-` only.    |
| `flags[].state`       | `boolean`   | Required field. Must be a boolean (`true` or `false`).                     |
| `flags[].description` | `string`    | Required field. Must be at least 20 characters long.                       |
| `flags[].dependencies`| `array`     | Required field. Must contain at least one entry. All items must be unique. |


## Examples

### Valid maintenance flag YAML

```yaml
changeRecord: INC000001
flags:
  - flag: ctl
    state: false
    description: Flag to trigger CTL maintenance page
    dependencies:
      - ui-spa-consent-to-let
      - ui-spa-servicing-auth
  - flag: xo
    state: true
    description: Flag to trigger XO maintenance page
    dependencies:
      - ui-spa-xo
```
!!! success
    This YAML is valid because it meets all the constraints defined in the schema.


### Invalid maintenance flag YAML

```yaml
changeRecord: INC000002
flags:
  - flag: ctl!main
    state: true
    description: Flag to trigger CTL
    dependencies: []
  - flag: xo_main
    state: "false"
    description: Flag to trigger XO maintenance page
    dependencies:
      - ui-spa-xo
      - ui-spa-xo
```
!!! danger "Issues in the above YAML"
    - `flag` in the first entry contains an invalid character (`!`), which is not allowed.
    
    - `description` in the first entry is less than 20 characters.  
    
    - `dependencies` in the first entry is empty, but it must contain at least one item.
    
    - `state` in the second entry is provided as a string (`"false"`), but it must be a boolean.
    
    - `dependencies` in the second entry contains duplicate items (`ui-spa-xo`).
