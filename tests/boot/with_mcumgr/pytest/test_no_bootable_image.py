from __future__ import annotations

import pytest
import logging

from pathlib import Path
from twister_harness import DeviceAdapter, Shell, MCUmgr
from utils import (
    match_lines,
    match_no_lines,
    check_with_shell_command
)

logger = logging.getLogger(__name__)

# Test that the primary image boots without a swap

def fail_load_no_bootable_image(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    #mcumgr.reset_device()
    #pass
    #dut.clear_buffer()
    dut.connect()
    output = dut.readlines_until('Unable to find bootable image|Launching primary slot application')
    match_lines(output, [
        'Unable to find bootable image'
    ])

def test_no_bootable_image(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    fail_load_no_bootable_image(dut, shell, mcumgr)