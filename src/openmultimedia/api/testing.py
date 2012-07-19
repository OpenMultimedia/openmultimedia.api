# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class TelesurPolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import openmultimedia.api
        self.loadZCML(package=openmultimedia.api)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'openmultimedia.api:default')


FIXTURE = TelesurPolicyFixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='openmultimedia.api:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='openmultimedia.api:Functional',
    )
