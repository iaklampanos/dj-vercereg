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
