# jellyfin-extract-subtitles-docker

This script lets you manually extract subtitles from Jellyfin movies and episodes. The reason for this script existing is that Jellyfin can often struggle with extraction which results in no subtitles being displayed at all.

The original script was written by [Ian Walton](https://github.com/iwalton3), which you can find [here](https://gist.github.com/iwalton3/f60f4741f561a742e6f8689a621c9824). You can find the original post about this script [here](https://www.reddit.com/r/jellyfin/comments/metzk6/subtitle_extraction_script/).

Since I don't like to manage Python installations on my system, I wrapped it in a Dockerfile so anybody can run it more easily.

## Requirements

The script interacts with the Jellyfin API so you can run it from any system that has access to your instance over the internet. You only need the following things:

* Your Jellyfin instance's base URL
* An admin user
    * More specifically, an API key for an admin user
* A system with Docker installed that has acess to your Jellyfin instance over the internet.

Personally, I have experienced issues when connecting through proxies like Cloudflare or nginx with this script, so you might want to connect to the instance with the port directly.

## Running the script

You can run the script with the following command:

```
docker run \
    --rm \
    -e URL='http://your-jellyfin-base-url.example.com'
    -e API_KEY='Your Jellyfin Admin API Key'
    zeryther/jellyfin-extract-subtitles-docker
```

The script can be very resource intensive and may take over a day to run initially. Once most of your library is extracted, you can setup a cronjob for it if you wish. You can read more about it on the original post of the script [here](https://www.reddit.com/r/jellyfin/comments/metzk6/subtitle_extraction_script/).
