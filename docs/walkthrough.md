# Herbie Walkthrough

## Overview

The idea of this walkthrough is to present the capabilities of Herbie and how it can help you, providing specific scenarios.

This assumes that you have Herbie already up and running; for a quick setup you can use the [Herbie sandbox](https://github.com/herbie/sandbox).

## Entity definition and Data publishing

Most probably you will have in your system a definition of what a _Customer entity_ should like. Different parts of the system need the whole entity while it is totally fine to use just some fields on another.

The definition of this same _Customer entity_ also changes along time so you will probably need to add additional information to it or remove it.

Most certainly you will want to send up to date _Customer data_ to multiple parts of your system when there is a change.

Herbie tries to solve these common scenarios by storing this _entity definition_ on a central place, allowing also to store different versions and publishing data changes to an _event bus_ that can any system can watch for changes.

The entity definition is stored using a versioned _JSON schema file_

## Customer schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://example.com/customer.schema.json",
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
  "required": [ "lastName" ]
}
```

Let's assume you have a super simple definition of a _Customer entity_ with just a unique identifier, a first name and a last name.

Of course this is far from what a real Customer entity would look like but it is a start. We can name this first version of our Customer entity as  `customer_v1.json`.

After loading this schema into Herbie we are ready to accept requests that contain Customer information and publish changes to the applications that are interested in knowing that something changed regarding a Customer.

## Create, Update or Delete data for an Entity

Using our example _Customer schema_ the following requests show how we can create, update or delete data for a specific entity calling the existing API endpoints.

### Create

```json
> POST /api/customer/save
> Host: localhost:8000
> Authorization: Token x

{
 	"version": "v1",
 	"key": "c60eba64",
 	"payload": {
 		"firstName": "John",
 		"lastName": "Doe"
 	}
}
```

```json
{
  "message": "entity with key c60eba64 created in version v1"
}
```

### Update

To update an entity you don't need to send the whole data again, but just the fields you need to change.

```json
> PATCH /api/customer/c60eba64/v1/update
> Host: localhost:8000
> Authorization: Token x

{
 	"lastName": "Doe"
}
```

```json
{
  "message": "entity with key c60eba64 updated in version v1"
}
```

### Delete

We can either delete just a specific version of an entity or if we _omit_ the version in the request payload, all the versions for the entity key provided will be deleted.

```json
> POST /api/customer/delete
> Host: localhost:8000
> Authorization: Token x

{
 	"version": "v1",
 	"key": "c60eba64"
}
```

```json
{
  "message": "entity with key c60eba64 deleted from version v1"
}
```

or

```json
> POST /api/customer/delete
> Host: localhost:8000
> Authorization: Token x

{
 	"key": "c60eba64"
}
```

```json
{
  "message": "entity with key c60eba64 deleted from all versions"
}
```

## Entity data Validation

Every time you call an endpoint sending data to a specific schema this data is validated against the _JSON schema_ you initially loaded into Herbie.

Using Herbie you guarantee that you can have a central definition of what an entity looks like and validate the data against the schema every time there is a change to an entity on your system.

```json
> POST /api/customer/save
> Host: localhost:8000
> Authorization: Token x

{
 	"version": "v1",
 	"key": "c60eba64",
 	"payload": {
 		"firstName": "John"
 	}
}
```

```json
{
  "message": {
    "lastName": {
      "error_message": "'lastName' is a required property",
      "validation_error": "required"
    }
  }
}
```

## Schema Changes and Backward Compatibility

Of course our _customer_v1_ is a really simple and dummy definition of what a customer entity could/should look like.

Having in mind that these definitions change along the way Herbie allows to either change an existing schema version or create a new version for the same entity.

In case you are replacing the same version we will check if the new schema is _backwards compatible_, meaning if the old data is still valid for this new schema.

If we, for example, change our _customer_v1_ and change the _firstName_ to be a required field this would introduce a BC break as previously that field was not required.

You can also at any time check the current stored schema version for a desired entity.

```json
> GET /api/schema-registry/customer/
> Host: localhost:8000
> Authorization: Token x
```

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://example.com/customer.schema.json",
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
  "required": [ "lastName" ]
}
```

## Publishing changes to multiple systems using an event bus system

Having a centralized place where you can store different different versions of an Entity and at the same time the respective data for these entities makes it the best place to push these data changes to multiple systems.

With Herbie this is quite easy just by attaching one or more adapters; by default [Google pubsub](https://github.com/herbie/google-pubsub-adapter) and [AWS SNS/SQS](https://github.com/herbie/aws-sns-sqs-adapter) are provided.

Whenever an entity data is changed we publish these changes to the configured adapters.

A 3rd party system that wants to know about these changes just needs to subscribe to one of these systems and consume/process the messages published to them.
