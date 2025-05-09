#!/usr/bin/env python3
# Copyright (c) 2024 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

import importlib
import json
import os
import sys
from unittest import mock
import subprocess
import pytest
twister_cmd = ["./zephyr/scripts/twister"] + \
    ["--west-flash", "--west-runner", "pyocd", "--enable-slow", "-T", "zephyr/tests/boot/with_mcumgr"] + \
    ["-p","stm32h573i_dk", "--device-testing", "--device-serial","/dev/ttyACM0", "-v"]
    

def swap_binaries(tests):
    for test_id in tests:
        test_id_tail = test_id.split(".")[-1][5:]
        print(test_id_tail)
        result = subprocess.run(["cp", f"./zephyr/tests/boot/with_mcumgr/test_bins/{test_id_tail}/zephyr.signed.hex",\
                    f"twister-out/stm32h573i_dk/tests/boot/with_mcumgr/{test_id}/with_mcumgr/zephyr/zephyr.signed.hex"])
        

tests = [
    "boot.with_mcumgr.boot_validation.test_load_success",
    "boot.with_mcumgr.boot_validation.test_corrupted_magic",
    "boot.with_mcumgr.boot_validation.test_misaligned_load_addr",
    "boot.with_mcumgr.boot_validation.test_aligned_load_addr",
    "boot.with_mcumgr.boot_validation.test_header_size_too_small",
]
def build_tests(tests: list[str]):
    cmd = twister_cmd
    for test in tests:
        cmd+=["-s"]
        cmd+=[test]

            # Execute the Twister call itself.

    result = subprocess.run(cmd+["--build-only"]) # run without changing hex, should fail
    assert str(result.returncode) == "0"

def run_tests(tests: list[str]):
    cmd = twister_cmd
    for test in tests:
        cmd+=["-s"]
        cmd+=[test]

            # Execute the Twister call itself.

    result = subprocess.run(cmd+["--test-only"]) # run without changing hex, should fail
    # assert str(result.returncode) == "0"
build_tests(tests)
swap_binaries(tests)
run_tests(tests)