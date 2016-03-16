#!/usr/bin/env python2

import sys
import time
sys.path.append('../../buildtools/binary_patcher')
sys.path.append('../../buildtools/elffile')
import binary_patcher
from binary_patcher import *
import elffile

ef = elffile.open(name="patch.elf")

def getSectionAddr(name):
	return next((header for header in ef.sectionHeaders if header.name == name), None).addr

patch_firmware("../../bootimg_src/firmware/fw_bcmdhd.orig.bin", 
    "fw_bcmdhd.bin", [
	ExternalArmPatch(getSectionAddr(".text"), "text.bin"),

	ExternalArmPatch(getSectionAddr(".text.before_before_initialize_memory_hook"), "before_before_initialize_memory_hook.bin"),
	GenericPatch4(0x181240, getSectionAddr(".text.before_before_initialize_memory_hook")+1),

	ExternalArmPatch(getSectionAddr(".text.interrupt_handler"), "interrupt_handler.bin"),
	GenericPatch4(0x1ECA84, getSectionAddr(".text.interrupt_handler")+1),

	ExternalArmPatch(getSectionAddr(".text.tr_pref_abort_hook"), "tr_pref_abort_hook.bin"), # patch to stay in abort mode to handle exception, original codes switches to system mode

	ExternalArmPatch(getSectionAddr(".text.tr_data_abort_hook"), "tr_data_abort_hook.bin"), # patch to stay in abort mode to handle exception, original codes switches to system mode

	StringPatch(0x1FD31B, "build: " + time.strftime("%d.%m.%Y %H:%M:%S") + "\n"), # 53 character string
	])
