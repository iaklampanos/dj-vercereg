# Copyright 2014 The University of Edinburgh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# General convenience makefile for the dj-vercereg project


DB_USER=root
DB_PASS=root
DB_EXEC=mysql
DB_NAME=dj_vercereg
DB_HOST=localhost
DB_PORT=3306
DB_COMMAND=$(DB_EXEC) -u$(DB_USER) -p$(DB_PASS) -h$(DB_HOST) --port=$(DB_PORT) $(DB_NAME)

help::
	@echo "Help:"
	@echo "   make <command> <params>"
	@echo ""
	@echo "Commands:"
	@echo "   db-shell: execute a mysql shell to the VERCE Registry DB"
	@echo "   db-dropcreate: drop and create the DB schema"
	
db-shell::
	$(DB_COMMAND)

dc:: db-dropcreate
db-dropcreate::
	echo "drop schema $(DB_NAME); create schema $(DB_NAME)" | $(DB_COMMAND)
