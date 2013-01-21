# -*- coding: utf-8 -*-

import json
import SimpleHTTPServer
import SocketServer

from time import sleep
from thread import start_new_thread

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  # pragma: no cover

    def do_GET(self):  # flake8: noqa
        try:
            path, rest = self.path.split('?')

        except ValueError:
            path = self.path

        if path == '/video_api/get_json/good_response':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            
        if path == '/video_api/get_json/not_found':
            self.send_response(404)
            
        if path == '/video_api/get_json/internal_error':
            self.send_response(500)

        if path == '/video_api/get_json/timeout':
            sleep(6.1)

        if path == '/video_api/get_json/error_response':
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()

            response = {"Error": "invalid"}

            self.end_headers()

            self.wfile.write(json.dumps(response))
            self.wfile.close()

class TelesurPolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def startSimpleHTTPServer(self):  # pragma: no cover
        PORT = 15555

        try:
            httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
        except:
            print "\n***************************************************************"
            print "*Internal server could not be started, please run tests again.*"
            print "***************************************************************"
            sys.exit(1)

        print "\nserving internal server at port", PORT
        httpd.serve_forever()

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.api
        self.loadZCML(package=openmultimedia.api)

    def setUpPloneSite(self, portal):
        # Start our internal server
        self.multimedia_server = start_new_thread(self.startSimpleHTTPServer, ())
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'openmultimedia.api:default')


FIXTURE = TelesurPolicyFixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='openmultimedia.api:Integration',)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='openmultimedia.api:Functional',)
