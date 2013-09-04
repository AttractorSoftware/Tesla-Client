Tesla-Client
============

Django CI server notification

	TESLA_IP_ADDRESS = 'address_of_the_tesla_server'
	TESLA_USERNAME = 'username_of_the_tesla_server'
	#url to the jenkins json report
	TESLA_CLIENT_URL = "http://192.168.0.96:8080/job/job_name/lastBuild/api/json"
        #path to the manage.py file
	TESLA_COMMAND_PATH = '/home/username/projects/tesla-src/application/tesla/manage.py'
        #host to deploy to
	TESLA_DEPLOY_HOST = 'somehostname.net'
