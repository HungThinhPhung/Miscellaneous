### Overview
Docker containers and services can connect together or connect with non-Docker workloads<br>

Docker networking system is plugable, using drivers. Serveral exists by default, and provide core networking functionality
* bridge (default network driver): used when your app run in standalone containers that need to be communicates, used to connect between containers in same docker daemon
* host: for standalone containers, it removes network system between docker containers and docker host. Then it uses host's networking directly
* overlay: used to connect between
    + multiple docker daemon to enable swarm service
    + swarm service and standalone container
    + two standalone containers on difference docker daemons
* macvlan: allow you assign MAC address for each container, making it appear as a physical device on network. Docker daemon routes traffic by that MAC Address. It is the best choice when dealing with legacy app that expect to be directly connect with physical network.
* none: disable networking of container. Not available for swarm services.
* Network plugin: From third party

### Bridge
In term of network, bridge is a software or a physical device. It forwards traffic between network segments<br>
In term of docker, bridge is a software.
Can create user-defined bridge network
Default bridge vs user-defined:
* User-defined bridge provide automatic DNS between container<br>
Containers in default brigde network can only access each other by IP, unless use --link option (deprecated). On user-defined network, containers can resolve other by name or alias
* User-defined bridge provide better isolation
All container are default for bridge


    