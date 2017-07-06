#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from pluggy import HookspecMarker


pre_scan = HookspecMarker('pre_scan')
scan_proper = HookspecMarker('scan_proper')
scan_output = HookspecMarker('scan_output')
post_scan = HookspecMarker('post_scan')

@pre_scan
def extract_archive():
    pass

@scan_proper
def add_cmdline_option(scan_output_plugins):
    """
    Return a click.Option instance which will be added to scancode.cli.ScanCommand
    """
    pass

@scan_output
def write_output(format, files_count, version, notice, scanned_files, options, input, output_file, _echo):
    pass

@scan_output
def add_format():
    """
    Return a unique format name and a plugin to act as a callback for that format
    """
    pass