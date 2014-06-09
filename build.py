# coding=utf-8
#
# fysom - pYthOn Finite State Machine - this is a port of Jake
#         Gordon's javascript-state-machine to python
#         https://github.com/jakesgordon/javascript-state-machine
#
# Copyright (C) 2011 Mansour Behabadi <mansour@oxplot.com>, Jake Gordon
#                    and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from pybuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')

use_plugin('filter_resources')

use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.unittest')
use_plugin('python.flake8')
use_plugin('python.pydev')
use_plugin('copy_resources')

name = 'fysom'
url = 'https://github.com/mriehl/fysom'
license = 'MIT'
authors = [Author('Mansour Behabadi', 'mansour@oxplot.com'),
           Author('Jake Gordon', 'jake@codeincomplete.com'),
           Author('Maximilien Riehl', 'maximilien.riehl@gmail.com'),
           Author('Stefano', email='')]
summary = 'pYthOn Finite State Machine'
version = '1.0.15'

default_task = ['analyze', 'publish']


@init
def set_properties(project):
    project.get_property('filter_resources_glob').append(
        '**/fysom/__init__.py')

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.get_property('copy_resources_glob').append('README')

    project.set_property('flake8_include_test_sources', True)

    project.set_property('unittest_module_glob', 'test_*')

    project.set_property('distutils_classifiers', [
                         'Development Status :: 5 - Production/Stable',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: MIT License',
                         'Programming Language :: Python',
                         'Natural Language :: English',
                         'Operating System :: OS Independent',
                         'Topic :: Scientific/Engineering'])


@init(environments="teamcity")
def set_properties_for_teamcity(project):
    import os
    project.version = '%s-%s' % (
        project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_build_dependencies', 'analyze', 'package']
    project.get_property('distutils_commands').append('bdist_rpm')
