podman run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /opt/argos/custom/docker/argos_mount:/app:rw -e DISPLAY=unix:0 -v /dev/snd:/dev/snd --privileged argos /opt/argos/AutoMoDe/bin/automode_main_bt -c /app/mission.argos --bt-config --nroot 3 --nchildroot 1 --n0 0 --nchild0 2 --n00 6 --c00 5 --p00 0.26 --n01 5 --a01 0 --rwm01 5 --p01 0
