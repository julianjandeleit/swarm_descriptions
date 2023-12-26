docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /opt/argos/custom/docker/argos_mount:/app:rw -e DISPLAY=unix:0 -v /dev/snd:/dev/snd --privileged argos bash
