import urllib2
import json
import paramiko
from django.conf import settings


class TeslaClient(object):
    build_info = None

    def __init__(self):
        self.build_info = BuildInfo()

    def get_json_from_url(self, url):
        jenkins_page = urllib2.urlopen(url)
        json_data = jenkins_page.read()
        return json_data

    def parse_json(self, json_string):
        json_data = json.loads(json_string)
        return json_data

    def get_build_info(self):
        return self.build_info

    def set_build_info(self, json_data):
        self.build_info.build_number = json_data['number']
        self.build_info.build_status = json_data['result'].lower()
        if 'failCount' in json_data:
            self.build_info.fail_count = json_data['failCount']
        if 'passCount' in json_data:
            self.build_info.pass_count = json_data['passCount']
        if 'skipCount' in json_data:
            self.build_info.skip_count = json_data['skipCount']

        self.build_info.total_count = self.build_info.fail_count + self.build_info.pass_count + self.build_info.skip_count

    def notify_server(self, json_data, project):

        if self.build_info.build_status == 'success':
            message = u"\"Build #%d completed.\"" % self.build_info.build_number
            type = u"success"
        else:
            if u'failCount' not in json_data:
                message = u"\"Build #%d failed.\"" % self.build_info.build_number
                type = u"error"
            else:
                message = u"\"Build #%d failed. %d tests failed out of %d.\"" % (
                self.build_info.build_number, self.build_info.fail_count, self.build_info.total_count)
                type = u"error"

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_command = "python %s notify --type=%s --project=%s --message=%s" \
                      % (settings.TESLA_COMMAND_PATH, type, project, message)

        ssh.connect(settings.TESLA_IP_ADDRESS, username=settings.TESLA_USERNAME)
        ssh.exec_command(ssh_command)
        ssh.close()


class BuildInfo(object):
    build_number = None
    build_status = ""
    fail_count = 0
    pass_count = 0
    skip_count = 0
    total_count = 0
    url = ""

    def __init__(self):
        self.build_number = None
        self.build_status = ""
        self.fail_count = 0
        self.pass_count = 0
        self.skip_count = 0
        self.total_count = 0
        self.url = ""


