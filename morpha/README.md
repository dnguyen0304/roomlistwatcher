# Morpha

## Getting Started
### Building
Update the configuration files in the `configuration` directory and then build the package.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker build --file Dockerfile \
                  --tag dnguyen0304/morpha-morpha-buildtime:<tag> \
                  .
sudo docker run --rm \
                --volume $(pwd):/tmp/build \
                dnguyen0304/morpha-morpha-buildtime:<tag>
```

### Pushing
Push the buildtime image.
```
# NOTE: Remember to replace the <tag> placeholder.

sudo docker push dnguyen0304/morpha-morpha-buildtime:<tag>
```
