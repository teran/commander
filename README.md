commander
=========

Command line util to work with multiple servers and uses Zabbix as database
for hosts data

requirements
============

 * pyzabbix
 * readline

help page
=========
    Usage: cmd.py [options]

    Options:
      -h, --help            show this help message and exit
      -u URL, --url=URL     Zabbix URL
      -l LOGIN, --login=LOGIN
                            Zabbix user to login with
      -p PASSWORD, --password=PASSWORD
                            Zabbix password
      -w, --write-configuration
                            Write given parameters as default configuration
      -c, --use-cache       Do not reload cache and use the previously stored one
      -d, --enable-logging  Enable logging(log store in cache directory)

how to start
============

Just start it the same way:

	cmd.py -u http://my-lovely-zabbix-instance -l username -p password

Now you have logged in into zabbix. It's very useful if you wanna connect to
 zabbix instance you want to use once.

If it's you lovely zabbix and you wanna use it everytime and do not add so
many options you can do one of the following add ``-w`` option or use internal
command ``write_configuration``. They are doing exaclty the same.
