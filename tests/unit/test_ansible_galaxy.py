#  Copyright (c) 2015-2016 Cisco Systems
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import re

import pytest

from molecule import ansible_galaxy


@pytest.fixture()
def galaxy_instance():
    data = {'config_file': 'test.cfg', 'requirements_file': 'requirements.yml'}

    return ansible_galaxy.AnsibleGalaxy(data['requirements_file'])


def test_requirements_file_loading(galaxy_instance):
    assert 'requirements.yml' == galaxy_instance.requirements_file


def test_add_env_arg(galaxy_instance):
    galaxy_instance.add_env_arg('MOLECULE_1', 'test')

    assert 'test' == galaxy_instance.env['MOLECULE_1']


def test_install(mocker, galaxy_instance, ansible_section_data):
    mocked = mocker.patch('molecule.ansible_galaxy.AnsibleGalaxy.execute')
    galaxy_instance.install(ansible_section_data['ansible']['config_file'])

    mocked.assert_called_once
    assert re.search(r'ansible-galaxy install -f -r requirements.yml',
                     str(galaxy_instance.galaxy))
