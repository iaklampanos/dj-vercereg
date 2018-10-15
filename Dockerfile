# Use Ubuntu 
FROM ubuntu:18.04

USER root

# Install python packages and mysql
RUN apt-get update && apt-get install -y python-dev python-pip python-setuptools libmysqlclient-dev mysql-client git

# Clone code
RUN git clone https://github.com/davidath/dj-vercereg.git registry
RUN pip install -r /registry/dj_vercereg/python_env_requirements.txt


CMD ["/bin/bash", "/registry/start-registry.sh"]
