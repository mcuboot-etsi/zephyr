from __future__ import annotations

import pytest
import logging

from pathlib import Path
from twister_harness import DeviceAdapter, Shell, MCUmgr
from west_sign_wrapper import west_sign_with_imgtool
from utils import (
    find_in_config,
    match_lines,
    match_no_lines,
    check_with_shell_command,
    check_with_mcumgr_command,
)

logger = logging.getLogger(__name__)

# Test that the primary image boots without a swap

def test_success_load(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr, boot_output: str):
    mcumgr.reset_device()

    dut.connect()
    output = dut.readlines_until('Launching primary slot application')
    match_no_lines(output, [
        boot_output
    ])
    logger.info('Verify new APP is still booted')
    check_with_shell_command(shell, new_version)

# 