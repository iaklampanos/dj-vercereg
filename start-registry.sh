#!/bin/bash
localsettemp=/registry/dj_vercereg/dj_vercereg/local_settings_template.py
localset=/registry/dj_vercereg/dj_vercereg/local_settings.py
port=8000
dj_path=/registry/dj_vercereg

# Local settings workflow / initializer

if [[ -f $localset && ! -L $localset ]]; then
	echo "Using custom local_settings.py..."
else
	if [ ! -L $localset ]; then
		echo "Creating local_settings_template.py link......"
		ln -s $localsettemp $localset
	else	
		echo "Using local_settings_template.py as local_settings.py, if you want to use custom settings you should create a custom local_settings.py file. Using local_settings_template.py as is, is not safe."
	fi
fi

# Registry db initializations

until python $dj_path/manage.py makemigrations > /dev/null 2>&1 ;do
      echo "Waiting mysql docker to setup........"
      sleep 1
done

echo "Initializing....."
python $dj_path/manage.py makemigrations
python $dj_path/manage.py migrate
python $dj_path/manage.py migrate --run-syncdb

# Create superuser from localsettings
username=`cat $localset | grep USER | awk -F ":" '{print $2}'`
username=`sed -n "s/^.*'\(.*\)'.*$/\1/ p" <<< ${username}`

password=`cat $localset | grep PASSWORD | awk -F ":" '{print $2}'`
password=`sed -n "s/^.*'\(.*\)'.*$/\1/ p" <<< ${password}`

email=$username"@example.com"

echo "Creating super user....."

echo "from django.contrib.auth.models import User; User.objects.create_superuser('$username', '$email', '$password')" | python $dj_path/manage.py shell

echo "Fixtures...."

python $dj_path/manage.py loaddata $dj_path/fixtures/def_group.json

echo "Starting web server...."

python $dj_path/manage.py runserver 0.0.0.0:$port
