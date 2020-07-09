# Example consumer for business entity messages

A basic example script for reading messages of a business entity.
It will continuously read the messages and print them to sys.stdout.

To start the consumer script locally, build and run the docker image:

```
cd example_consumers/consumer/
docker build -t "exampleconsumer" .
docker run --net herbie_herbie-network exampleconsumer
```

(The herbie, kafka and zookeper containers should also be running, so that the consumer can connect to the herbie-kafka)
