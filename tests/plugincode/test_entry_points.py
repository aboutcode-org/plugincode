# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import subprocess
import sys
from unittest.mock import Mock

import pytest

import plugincode
from plugincode import BasePlugin, HookimplMarker, HookspecMarker, PluginManager, PlugincodeError
from plugincode.location_provider import LocationProviderPlugin, SimplePluginManager


def test_all_stages_import_without_pluggy():
    script = """
import importlib.abc
import sys
class NoPluggy(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname == 'pluggy':
            raise ImportError('pluggy must not be imported')
sys.meta_path.insert(0, NoPluggy())
from plugincode import location_provider, pre_scan, scan, post_scan, output, output_filter
"""
    subprocess.run([sys.executable, "-c", script], check=True)


@pytest.mark.parametrize("marker_class", [HookspecMarker, HookimplMarker])
def test_legacy_markers_preserve_classes_and_functions(marker_class):
    marker = marker_class("test")

    class Plugin:
        pass

    def function():
        return 42

    assert marker(Plugin) is Plugin
    assert marker(tryfirst=True)(Plugin) is Plugin
    assert marker(function) is function
    assert marker(specname="legacy")(function) is function


@pytest.mark.parametrize("kind", ["stage", "location"])
def test_entry_points_keep_first_name_and_initialize_once(monkeypatch, kind):
    base = BasePlugin if kind == "stage" else LocationProviderPlugin

    class Valid(base):
        pass

    first = Mock(name="first")
    first.name = "example"
    first.load.return_value = Valid
    duplicate = Mock(name="duplicate")
    duplicate.name = "example"
    entries = Mock(return_value=[first, duplicate])
    monkeypatch.setattr(plugincode, "entry_points", entries)
    if kind == "stage":
        manager = PluginManager("test", __name__, "test.group", base)
    else:
        manager = SimplePluginManager(__name__, "test.group", base)
    try:
        manager.setup()
        manager.setup()
        assert Valid.name == "example"
        if kind == "stage":
            assert manager.plugin_classes == [Valid]
            assert Valid.stage == "test"
        else:
            assert manager.plugin_classes == {"example": Valid}
        entries.assert_called_once_with(group="test.group")
        first.load.assert_called_once_with()
        duplicate.load.assert_not_called()
    finally:
        if kind == "stage":
            PluginManager.managers.pop("test", None)


@pytest.mark.parametrize("kind", ["stage", "location"])
def test_invalid_plugins_are_rejected(monkeypatch, kind):
    entry = Mock()
    entry.name = "invalid"
    entry.load.return_value = object
    monkeypatch.setattr(plugincode, "entry_points", Mock(return_value=[entry]))
    if kind == "stage":
        manager = PluginManager("test", __name__, "test.group", BasePlugin)
        error = PlugincodeError
    else:
        manager = SimplePluginManager(__name__, "test.group", LocationProviderPlugin)
        error = Exception
    try:
        with pytest.raises(error, match="must extend"):
            manager.setup()
        assert not manager.initialized
    finally:
        if kind == "stage":
            PluginManager.managers.pop("test", None)


def test_stage_plugins_retain_sort_order_and_options(monkeypatch):
    from commoncode.cliutils import PluggableCommandLineOption

    option = PluggableCommandLineOption(["--example"], is_flag=True)

    class Later(BasePlugin):
        sort_order = 20
        options = [option]

    class Earlier(BasePlugin):
        sort_order = 10

    entries = []
    for name, cls in [("later", Later), ("earlier", Earlier)]:
        entry = Mock()
        entry.name = name
        entry.load.return_value = cls
        entries.append(entry)
    monkeypatch.setattr(plugincode, "entry_points", Mock(return_value=entries))
    manager = PluginManager("test", __name__, "test.group", BasePlugin)
    try:
        classes, options = manager.setup()
        assert classes == [Earlier, Later]
        assert options == [option]
    finally:
        PluginManager.managers.pop("test", None)


@pytest.mark.parametrize("kind", ["stage", "location"])
def test_entry_point_import_errors_propagate(monkeypatch, kind):
    entry = Mock()
    entry.name = "broken"
    entry.load.side_effect = ImportError("missing plugin dependency")
    monkeypatch.setattr(plugincode, "entry_points", Mock(return_value=[entry]))
    manager = (
        PluginManager("test", __name__, "test.group", BasePlugin)
        if kind == "stage"
        else SimplePluginManager(__name__, "test.group", LocationProviderPlugin)
    )
    try:
        with pytest.raises(ImportError, match="missing plugin dependency"):
            manager.setup()
        assert not manager.initialized
    finally:
        if kind == "stage":
            PluginManager.managers.pop("test", None)
