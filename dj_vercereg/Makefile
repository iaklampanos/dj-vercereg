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
DB_HOST=dj-reg-db
DB_PORT=3306
DB_COMMAND=$(DB_EXEC) -u$(DB_USER) -p$(DB_PASS) -h$(DB_HOST) --port=$(DB_PORT) $(DB_NAME)

WEB_HOST=0.0.0.0
WEB_PORT=8000

help:://
	@echo "Help:"
	@echo "   make <command> <params>"
	@echo ""
	@echo "Commands:"
	@echo "   db-shell: execute a mysql shell to the VERCE Registry DB"
	@echo "   db-dropcreate: drop and create the DB schema"
	@echo "   clean: drop and create the DB schema as well as add fixtures and a superuser"
	@echo "   test: run predefined tests, first time running initializes temporary tables, rerun for test results (despite errors during initialization)"
	@echo "   run: start webserver"


	
db-shell::
	$(DB_COMMAND)

dc:: db-dropcreate
db-dropcreate::
	echo "drop schema $(DB_NAME); create schema $(DB_NAME)" | $(DB_COMMAND)

clean:: dc
	python manage.py makemigrations
	python manage.py migrate
	python manage.py migrate --run-syncdb
	python manage.py createsuperuser
	python manage.py loaddata fixtures/def_group.json
	$(DB_EXEC) -u$(DB_USER) -p$(DB_PASS) -h$(DB_HOST) --port=$(DB_PORT) < ../sql/fix_mysql_for_watson.sql
	$(DB_EXEC) -u$(DB_USER) -p$(DB_PASS) -h$(DB_HOST) --port=$(DB_PORT) dj_vercereg < ../sql/fix_mysql_for_watson.sql

test::
	python manage.py test --keepdb

run::
	python manage.py runserver $(WEB_HOST):$(WEB_PORT)
