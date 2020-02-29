### Dockerfile
**FROM** *\<base-image>:\<version>* Define base image<br>
**RUN** *\<parameter>* executes command(s) in a new layer and creates a new image, it is often used for installing software packages<br>
**CMD** *\<parameter>* sets default command and/or parameters, which can be overwritten from command line when docker container runs.<br>
<pre>CMD echo "Hello world" </pre>
when container runs as docker run -it <image> will produce output
<pre>Hello world</pre>
but when container runs with a command, e.g., docker run -it <image> /bin/bash, CMD is ignored and bash interpreter runs instead:
<pre>root@7de4bed89922:/#</pre>
**ENTRYPOINT** *\<paramenter>* configures a container that will run as an executable.<br>
**COPY** *\<src> \<destination>* Copy file or folder from local into docker image<br>
**ADD** *\<src> \<destination>* Copy file or folder from local, url or compress file (extract) to directory <br>

<pre>COPY src /src</pre>
and
<pre>ADD src /</pre> 
do the same thing <br>

### Docker-compose
<pre>
version: '3.4'  # Define version of docker-compose which is used (optional but required for some commands)
services:
  <i>"""  
  Define list of service
  If only run docker-compose build, push, pull, up or stop
  -> all service will be executed
  If docker-compose build upload_api
  -> only service upload_api is built
  """</i>
  upload_api: # name of service
    build:
      network: host
      context: .
      dockerfile: dockerfile # dockerfile location
    image: upload_api:0.1 # image name and tag, also consist docker repository url if use push or pull
    container_name: upload_api
    ports:
      - 8089:8088 # 8089 is port of local, 8088 is port inside container
    volumes: # persistent volume for data
        <i>"""
        bind mount: You select local path for file or folder
        volume mount:  New directory is created within Docker’s storage directory on the host machine, and Docker manages that directory’s contents
        """</i>
      - type: bind 
        source: '/home/phthinh/Projects/PycharmProjects/MISA.MFace/upload_api/upload_api/data'
        target: '/data/upload_data/'
</pre>

<b><i>If you build docker with docker-compose, all command in docker file will run from directory that run docker-compose command</i></b>