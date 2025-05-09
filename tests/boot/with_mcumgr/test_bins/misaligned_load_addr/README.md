Test that if the load_addr is not aligned to 4 bytes, MCUboot fails to boot

CHANGES:
Image header load_addr = 00 00 00 01 instead of 00 00 00 00