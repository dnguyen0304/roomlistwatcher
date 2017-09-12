# Room List Watcher
A Pokemon Showdown web scraper.

## Getting Started
### Building
```
sudo ./build.sh
```

### Running
Update the configuration files in the `configuration` directory first.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker run --rm \
                --volume $(pwd)/configuration:/etc/opt/roomlistwatcher \
                --volume $(pwd):/var/opt/roomlistwatcher/log \
                dnguyen0304/roomlistwatcher:<tag>
```

### Pushing
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/roomlistwatcher-buildtime:<tag>
sudo docker push dnguyen0304/roomlistwatcher:<tag>
```

### Pulling
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/roomlistwatcher:<tag>
```

## Advanced
### Managing the runtime image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build \
    --file docker/runtime/Dockerfile \
    --tag dnguyen0304/roomlistwatcher-runtime:<tag> \
    --build-arg NAMESPACE=roomlistwatcher \
    --build-arg CONFIGURATION_FILE_NAME="application.config" \
    --build-arg AWS_CONFIGURATION_FILE_NAME="aws.config" \
    --build-arg AWS_CREDENTIALS_FILE_NAME="aws.credentials" \
    .

sudo docker push dnguyen0304/roomlistwatcher-runtime:<tag>
```
