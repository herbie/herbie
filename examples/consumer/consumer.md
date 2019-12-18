# Example consumer for business entity messages

A basic example script for reading messages of a business entity.
It will continuously read the messages and print them to sys.stdout.

To start the consumer script locally, build and run the docker image:

```
cd examples/consumer/
docker build -t "exampleconsumer" .
docker run --net wayne_wayne-network exampleconsumer
```

(The wayne container should also be running, so that the consumer can connect to the wayne-kafka)
