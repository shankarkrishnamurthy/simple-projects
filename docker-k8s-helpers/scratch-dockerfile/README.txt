Description:
    Very basic and smallest container demo

Steps:
    gcc --static main.c -lc -o hw
    docker build -t hw-static .
    docker run --rm -t -d hw-static
    
    [root@zela-f33 scratch-dockerfile]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                  NAMES
e23d04b3bbcd        hw-static          ! "/hw /hw-1" !             22 seconds ago      Up 21 seconds                                              ecstatic_hamilton
    * watch /hw-1 and /hw in the Dockerfile*
    docker logs -f e23d04b3bbcd
    docker stop e23d04b3bbcd


