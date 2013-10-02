from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core.management import call_command
from django.conf import settings

from tesla_client.management.commands import TeslaClient


class Command(BaseCommand):
    help = 'Read the test results from jenkins and send it to tesla service'
    option_list = BaseCommand.option_list + (
        make_option('--url',
                    dest='url',
                    default='',
                    help='Jenkins build results url'),
        make_option('--project',
                    dest='project',
                    default='',
                    help='Project name'),
    )

    def handle(self, *args, **options):
        if 'project' not in options.keys():
            raise CommandError(message="required fields not provided")

        jenkins_url = options['url'] = settings.TESLA_CLIENT_URL
        if 'url' in options.keys():
            jenkins_url = options['url']

        project = options['project']
        client = TeslaClient()
        json_string = client.get_json_from_url(jenkins_url)
        json_data = client.parse_json(json_string)
        client.set_build_info(json_data)
        client.notify_server(json_data, project)









