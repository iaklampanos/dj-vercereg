# Use Ubuntu 
FROM ubuntu:18.04

USER root

# Install python packages and mysql
RUN apt-get update && apt-get install -y python-dev python-pip python-setuptools libmysqlclient-dev git

# Clone code
RUN git clone https://github.com/davidath/dj-vercereg.git registry
RUN pip install -r /registry/dj_vercereg/python_env_requirements.txt


CMD ["/bin/bash", "/registry/dj_vercereg/start-registry.sh"]
