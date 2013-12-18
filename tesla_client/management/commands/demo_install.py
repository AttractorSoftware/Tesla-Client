# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from fabric.api import local, lcd
import calendar
from django.conf import settings
from tesla_client.management.commands import TeslaClient
import datetime
import re


class Command(BaseCommand):
    help = 'Deploy the changeset to demo if build was successful'
    option_list = BaseCommand.option_list + (
        make_option('--url',
                    dest='url',
                    default='',
                    help='Jenkins build results url'),

        make_option('--demo',
                    dest='demo',
                    default='',
                    help='The host where to install'),
    )

    def handle(self, *args, **options):
        demo_host = settings.TESLA_DEPLOY_HOST
        installation_commands = settings.TESLA_INSTALLATION_COMMANDS
        jenkins_url = settings.TESLA_CLIENT_URL

        if 'url' in options.keys() and options['url']:
            jenkins_url = options['url']

        if 'demo' in options.keys() and options['demo']:
            demo_host = options['demo']

        client = TeslaClient()
        json_string = client.get_json_from_url(jenkins_url)
        json_data = client.parse_json(json_string)
        client.set_build_info(json_data)
        build_info = client.get_build_info()
        if build_info.build_status == 'success':
            with(lcd('..')):
                success_revision = "Build_%d_%s_%s" % (build_info.build_number, 'success', calendar.timegm(datetime.datetime.now().utctimetuple()))
                local('git tag -a %s -m"Successfule build %d"' % (success_revision, build_info.build_number))
                local('git push --tags')
                for command in installation_commands:
                    command = re.sub('%tag%', success_revision, command)
                    local(command)