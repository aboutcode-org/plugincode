#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/plugincode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.


def test_plugincode_can_be_imported():
    import plugincode  # NOQA
    from plugincode import location_provider  # NOQA
    from plugincode import output_filter  # NOQA
    from plugincode import output  # NOQA
    from plugincode import post_scan  # NOQA
    from plugincode import pre_scan  # NOQA
    from plugincode import scan  # NOQA
