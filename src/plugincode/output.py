#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/plugincode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.

import functools

from commoncode.resource import Resource

from plugincode import CodebasePlugin
from plugincode import PluginManager
from plugincode import HookimplMarker
from plugincode import HookspecMarker

# Tracing flags
TRACE = False
TRACE_DEEP = False


def logger_debug(*args):
    pass


if TRACE or TRACE_DEEP:
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(" ".join(isinstance(a, str) and a or repr(a) for a in args))


stage = "output"
entrypoint = "scancode_output"

output_spec = HookspecMarker(project_name=stage)
output_impl = HookimplMarker(project_name=stage)


@output_spec
class OutputPlugin(CodebasePlugin):
    """
    Base plugin class for scan output formatters all output plugins must extend.
    """

    def process_codebase(self, codebase, output, **kwargs):
        """
        Write `codebase` to the `output` file-like object (which could be a
        sys.stdout or a StringIO).

        Note: each subclass is using a differnt arg name for `output`
        """
        raise NotImplementedError

    @classmethod
    def get_files(cls, codebase, **kwargs):
        """
        Return an iterable of serialized files mapping from a codebase.
        Include "info", "timing" and strip root as needed.
        """
        # FIXME: serialization SHOULD NOT be needed: only some format need it
        # (e.g. JSON) and only these should serialize
        timing = kwargs.get("timing", False)
        info = bool(kwargs.get("info") or getattr(codebase, "with_info", False))
        serializer = functools.partial(Resource.to_dict, with_info=info, with_timing=timing)

        strip_root = kwargs.get("strip_root", False)
        resources = codebase.walk_filtered(topdown=True, skip_root=strip_root)
        return map(serializer, resources)


output_plugins = PluginManager(
    stage=stage, module_qname=__name__, entrypoint=entrypoint, plugin_base_class=OutputPlugin
)
