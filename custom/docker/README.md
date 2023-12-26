https://github.com/docker/compose/issues/1048

xhost +local:docker

THEN OPEN SECOND TERMINAL

source start_argos.sh

or with `docker-compose`
`ARGOS_FILE=$PWD/argos_mount/mission.argos docker-compose up --build`
(ARGOS_FILE needs to be absolute path)