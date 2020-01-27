# Combining Business Entities

Sometimes a business entity may be a combination of different parts.
Consider for example a `Product`, that consists of a `ProductDescription`,
`Price` and `Stock` information. Those 3 parts may come from different sources like
a ProductCatalog, a PriceService and an ERP-System and therefore be separate business
entities with their own JSON schema definition.

To combine those 3 business entities into a new `Product` entity, you just have to add a
new JSON schema for the `Product` and add a `composition` definition into the JSON schema file,
for example:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://herbie.json-schema/product/product_v1.json",
  "title": "Product",
  "composition": [
    {
      "businessEntity": "product_description",
      "version": "v1",
      "joinField": "productId",
      "fields": ["productId", "name", "description", "imageUrl"]
    },
    {
      "businessEntity": "price",
      "version": "v1",
      "joinField": "productId",
      "fields": ["value", "currency"]
    },
    {
      "businessEntity": "stock",
      "version": "v1",
      "joinField": "productId",
      "fields": ["availability"]
    }
  ],
  "description": "product info",
  "type": "object",
  "properties": {
    "productId": {"type": "string"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "imageUrl": {"type": "string"},
    "value": {"type": "number"},
    "currency": {"type": "string"},
    "availability": {"type": "string"}
  },
  "required": [ "productId", "name", "value", "currency", "availability" ]
}
```
(full example of product, product_description, price and stock
JSON schemas can be found here: [examples/jsonschema/](examples/jsonschema/))

As you can see, for each composition part, you need to define:
* the name of the business entity
* the version of the business entity
* a join field that is used to join the different parts together
* a list of fields that should be added to the combined business entity

After adding this new `Product` JSON schema to your project, Herbie will automatically
generate a `Product` update message whenever a `Price`, `Stock` or `ProductDescription`
is updated. Although the message is only generated when the product entity is valid.
So for example when a new product description is created, but no price for this product
was created yet, and the price is listed as a required field in the product JSON schema, then
no `Product` update message will be generated (only a `ProductDescription` update message).

A combined entity gets automatically deleted (and a delete message is generated)
whenever one of its part entities gets deleted.

***
**Note:** The combination of the business entities is currently only executed when one of the
parts is created or updated. So when you define a new combination, Herbie will not check if
some of the parts might already exist and automatically combine them. We decided to not
implement this for now, because the combination of business entities is currently an
experimental feature and we are not sure if it's really that useful.
