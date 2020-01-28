# Example consumer for business entity messages

A basic example script for reading messages of a business entity.
It will continuously read the messages and print them to sys.stdout.

To start the consumer script locally, build and run the docker image:

```
cd example_consumers/google_pub_sub_consumer/
docker build -t "exampleconsumer" .
docker run -e PUBSUB_EMULATOR_HOST='herbie-google-pub-sub:8085' --net herbie_herbie-network exampleconsumer:latest
```

(The herbie, google-pub-sub container should also be running, so that the consumer can connect to the herbie-google-pub-sub)
