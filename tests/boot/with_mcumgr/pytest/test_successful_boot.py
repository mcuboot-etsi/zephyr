from __future__ import annotations
import time

import pytest
import logging

from pathlib import Path
from twister_harness import DeviceAdapter, Shell, MCUmgr
from utils import (
    match_no_lines,
    check_with_shell_command,
    wait_for_shell_prompt
)

logger = logging.getLogger(__name__)

# Test that the primary image boots without a swap

def success_load_no_swap(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    wait_for_shell_prompt(dut, shell)
    dut.clear_buffer()
    mcumgr.reset_device()
    
    dut.connect()
    
    # output = dut.readlines_until('Launching primary slot application')
    # match_no_lines(output, [
    #     'Unable to find bootable image'
    # ])
    # logger.info('Verify original APP is still booted')
    # check_with_shell_command(shell, '0.0.0+0')

def test_success_load(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    success_load_no_swap(dut, shell, mcumgr)