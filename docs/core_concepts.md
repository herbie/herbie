# Core concepts of Herbie

## Business Entity

Business entities are the central data objects that will be stored, validated and distributed from Herbie.


## Schema Registry

The structure of a business entity is defined by a json-file that is based on [json-schema](https://json-schema.org/).
All of this files are part of a specific python package called _schema-registry_, it can be located in your Herbie 
repository or in a separate one. The version of a schema can be specified in its filename.

**Example schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://herbie.json-schema/customer/customer_v1.json",
  "title": "Customer",
  "description": "Customer info",
  "type": "object",
  "properties": {
    "customerId": {
      "description": "The unique identifier for a customer",
      "type": "string"
    },
    "firstName": {"type": "string"},
    "lastName": {"type": "string"}
  },
  "required": [ "firstName" ],
  "additionalProperties": false
}
```

## High-level Request Flow

When a new entity is published to the Herbie API, a chain of operations is executed:

1. The structure of an entity is validated against its schema-file in the given version.
2. When the validation was successful, the entity is persisted in the database.
3. Eventually the entity gets published to an event-bus which can be subscribed by other services. 

![request flow image](herbie_request_flow.png)