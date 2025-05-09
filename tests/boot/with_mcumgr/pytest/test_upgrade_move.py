# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import pytest
import logging

from pathlib import Path
from twister_harness import DeviceAdapter, Shell, MCUmgr
from test_upgrade import upgrade_with_confirm, upgrade_with_revert, upgrade_signature
from zephyr.tests.boot.with_mcumgr.pytest.test_load import success_load_no_swap

move_output = 'Starting swap using move algorithm'


def test_upgrade_with_confirm(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    upgrade_with_confirm(dut, shell, mcumgr, move_output)


def test_upgrade_with_revert(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    upgrade_with_revert(dut, shell, mcumgr, move_output)


@pytest.mark.parametrize(
    'key_file', [None, 'root-ec-p256.pem'],
    ids=[
        'no_key',
        'invalid_key'
    ])
def test_upgrade_signature(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr, key_file):
    upgrade_signature(dut, shell, mcumgr, key_file, move_output)
