# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0'
long_description = open("README.rst").read() + "\n" + \
    open(os.path.join("docs", "INSTALL.rst")).read() + "\n" + \
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" + \
    open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='openmultimedia.api',
      version=version,
      description="API para interactuar con el API de OpenMultimedia",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business :: News/Diary",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone api rest openmultimedia',
      author='Franco Pellegrini',
      author_email='frapell@ravvit.net',
      url='https://github.com/desarrollotv/openmultimedia.api',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['openmultimedia'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.z3cform.widgets',
          'five.grok>=1.2.0',
          'Pillow',
          'plone.app.layout',
          'plone.autoform',
          'plone.behavior',
          'plone.dexterity',
          'plone.directives.form',
          'plone.formwidget.contenttree',
          'plone.i18n',
          'plone.registry',
          'plone.theme',
          'Products.Archetypes',
          'Products.ATContentTypes',
          'Products.CMFCore',
          'Products.CMFPlone>=4.1',
          'Products.GenericSetup',
          'setuptools',
          'z3c.form',
          'z3c.relationfield',
          'zope.browserpage',
          'zope.component',
          'zope.event',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.browserlayer',
              'unittest2',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
