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

sudo docker push dnguyen0304/roomlistwatcher-buildtime:<tag>
sudo docker push dnguyen0304/roomlistwatcher:<tag>
```
