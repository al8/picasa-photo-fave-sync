#!/usr/bin/env python3
import json
import logging
import os
import socket
import subprocess
import sys
import tempfile
import time
import traceback
import zlib
from collections import namedtuple

from plugins import filter_hash, filter_picasa, filter_recent, filter_regex
from sync_all_lib import (cleanup_output_path, copy_resize_rotate,
                          get_dirs_files, get_files, remote_delete_files,
                          remote_get_files, send_remote_command, set_params,
                          setup_logging, transfer_params_t, upload)


def main(logger):
    params = {
        "output_path": r"D:\!Dropbox.com\Dropbox (Personal)\sync_output",
        "scp_cmdline": [
            r"D:\Progs\pscp.exe",
            "-batch",
            "-pw",
            "pi",
        ],
        "output_jpg_size": 2048,
        "output_jpg_quality": 55,
        "imagemagick_convert_binary":  # from ImageMagick-6.9.3-7-portable-Q16-x64
        r"D:\!Dropbox.com\Dropbox (Personal)\raspberrypi-frameserver\transfer_client\convert.exe",
        "jhead_binary":  # on windows, jpegtran.exe must be in the same path
        r"D:\!Dropbox.com\Dropbox (Personal)\raspberrypi-frameserver\transfer_client\jhead.exe",
    }
    set_params(params)

    transfer_params_l = [
        transfer_params_t(
            r"D:\!Memories\staging area\Eye-Fi",
            [(filter_regex, {"dir": r"\d{4}[-]\d\d[-]\d\d[-].+",
                             "file": r"(((DSC|IMG_|[A-Z]+)\d+)|(\d+-\d+-\d+ \d+.\d+.\d+))[.]jpg"})],  # local_filters
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2011",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2012",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2013",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2014",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2015",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2016",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2017",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2018",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2019",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
        transfer_params_t(
            r"D:\!Memories\Photos\2020",
            # local_filters
            [(filter_regex, {"dir": r"\d{8} .+",
                             "file": r"\d{8}_\d{4}.+[.]jpg", }), filter_picasa],
            [],  # global_filters
        ),
    ]

    files = set()
    for p in transfer_params_l:
        files |= get_files(p)
    logger.info("TOTAL FILES TO SYNC: %d (cached in %s)" %
                (len(files), params["output_path"]))

    # resize rotate and copy the files
    new_files, not_new_files = copy_resize_rotate(files, params["output_path"])
    all_output_files = new_files | not_new_files
    if len(new_files):
        logger.info("FILES RESIZED: %d" % len(new_files))

    cleanup_output_path(params["output_path"], all_output_files)


if __name__ == "__main__":
    logger = setup_logging()
    main(logger)
