# Example consumer for business entity messages

A basic example script for reading messages of a business entity.
It will continuously read the messages and print them to sys.stdout.

To start the consumer script locally, build and run the docker image:

**Build**: 
```
cd example_consumers/google_pubsub_consumer/
docker build -t "exampleconsumer" .
```

**Running**:
```
docker run -e PUBSUB_EMULATOR_HOST='{pubsub-emulator-host}'  --net {herbie-docker-network} exampleconsumer:latest

with:
{pubsub-emulator-host} - Pubsub Host
{herbie-docker-network} - Herbie App Docker Network
```

e.g:

```
docker run -e PUBSUB_EMULATOR_HOST='herbie-google-pubsub:8085' --net sandbox_herbie-network exampleconsumer:latest
```

**Note:**

The herbie, google-pub-sub container should also be running, so that the consumer can connect to the herbie-google-pub-sub
