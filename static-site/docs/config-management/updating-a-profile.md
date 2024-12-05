# Adding New Properties

Add the property to each profile in `resources/config.yaml`.
For example, to add a new property `cache_timeout` insert the following:
```yaml
default:
 cache_timeout: 300
```

!!! info
    Any new properties must be defined in all profiles to prevent CLI failures.
    
    You need to update the models to `app_config_models.py` in order to access the new property in the code.

To access the property, use the application’s `ConfigManager` loading logic to read the new property. Here is an example: 

```python
from utils.config_manager import ConfigManager

config = ConfigManager.get_config()

cache_timeout = config.cache_timeout
```

!!! tip
    Use descriptive property names to avoid confusion when adding new properties.