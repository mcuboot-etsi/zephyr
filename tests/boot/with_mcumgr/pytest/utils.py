# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import logging
import re

from pathlib import Path
from twister_harness import Shell, MCUmgr, DeviceAdapter
from twister_harness.helpers.shell import ShellMCUbootCommandParsed
from west_sign_wrapper import west_sign_with_imgtool
import pytest
import time

logger = logging.getLogger(__name__)

def wait_for_shell_prompt(dut: DeviceAdapter, shell: Shell):
    logger.info('Wait for prompt')
    if not shell.wait_for_prompt():
        pytest.fail('Prompt not found')
    if dut.device_config.type == 'hardware':
        # after booting up the device, there might appear additional logs
        # after first prompt, so we need to wait and clear the buffer
        time.sleep(0.5)
        dut.clear_buffer()

def find_in_config(config_file: Path | str, config_key: str) -> str:
    re_key = re.compile(rf'{config_key}=(.+)')
    with open(config_file) as f:
        lines = f.readlines()
    for line in lines:
        if m := re_key.match(line):
            logger.debug('Found matching key: %s' % line.strip())
            return m.group(1).strip('"\'')
    return ''


def match_lines(output_lines: list[str], searched_lines: list[str]) -> None:
    """Check all lines exist in the output"""
    for sl in searched_lines:
        assert any(sl in line for line in output_lines)


def match_no_lines(output_lines: list[str], searched_lines: list[str]) -> None:
    """Check lines not found in the output"""
    for sl in searched_lines:
        assert all(sl not in line for line in output_lines)


def check_with_shell_command(shell: Shell, version: str, swap_type: str | None = None) -> None:
    mcuboot_areas = ShellMCUbootCommandParsed.create_from_cmd_output(shell.exec_command('mcuboot'))
    assert mcuboot_areas.areas[0].version == version
    if swap_type:
        assert mcuboot_areas.areas[0].swap_type == swap_type


def check_with_mcumgr_command(mcumgr: MCUmgr, version: str) -> None:
    image_list = mcumgr.get_image_list()
    # version displayed by MCUmgr does not print +0 and changes + to '.' for non-zero values
    assert image_list[0].version == version.replace('+0', '').replace('+', '.')

def create_signed_image(build_dir: Path, app_build_dir: Path, version: str) -> Path:
    image_to_test = Path(build_dir) / 'test_{}.signed.bin'.format(
        version.replace('.', '_').replace('+', '_'))
    origin_key_file = find_in_config(
        Path(build_dir) / 'mcuboot' / 'zephyr' / '.config',
        'CONFIG_BOOT_SIGNATURE_KEY_FILE'
    )
    west_sign_with_imgtool(
        build_dir=Path(app_build_dir),
        output_bin=image_to_test,
        key_file=Path(origin_key_file),
        version=version
    )
    assert image_to_test.is_file()
    return image_to_test

def create_unsigned_image(build_dir: Path, app_build_dir: Path, version: str) -> Path:
    image_to_test = Path(build_dir) / 'test_{}.signed.bin'.format(
        version.replace('.', '_').replace('+', '_'))
    origin_key_file = find_in_config(
        Path(build_dir) / 'mcuboot' / 'zephyr' / '.config',
        'CONFIG_BOOT_SIGNATURE_KEY_FILE'
    )
    west_sign_with_imgtool(
        build_dir=Path(app_build_dir),
        output_bin=image_to_test,
        key_file=None,
        version=version
    )
    assert image_to_test.is_file()
    return image_to_test
    
def clear_buffer(dut: DeviceAdapter) -> None:
    disconnect = False
    if not dut.is_device_connected():
        dut.connect()
        disconnect = True
    dut.clear_buffer()
    if disconnect:
        dut.disconnect()