#!/usr/bin/env python3
import argparse
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
                          setup_logging, transfer_params_t, conf_to_transfer_params)


def main(logger, args):
    current_path = os.path.dirname(os.path.realpath(__file__))
    set_params({
        "output_jpg_size": args.size,
        "output_jpg_quality": args.quality,

        # For jpeg resizing. From ImageMagick-6.9.3-7-portable-Q16-x64
        "imagemagick_convert_binary": os.path.join(current_path, "convert.exe"),
    })

    transfer_params_l = conf_to_transfer_params(args.configfile)

    files = set()
    for p in transfer_params_l:
        files |= get_files(p)
    logger.info("TOTAL FILES TO SYNC: %d (cached in %s)" %
                (len(files), args.output_path))

    if (args.dryrun):
        print("--dryrun active, skipping action")
        return

    # resize rotate and copy the files
    new_files, not_new_files = copy_resize_rotate(files, args.output_path)
    all_output_files = new_files | not_new_files
    if len(new_files):
        logger.info("FILES RESIZED: %d" % len(new_files))

    cleanup_output_path(args.output_path, all_output_files)


if __name__ == "__main__":
    logger = setup_logging()

    parser = argparse.ArgumentParser(
        description='Resize some favorite photos.')
    parser.add_argument("--output_path", "-o",
                        default=r"D:\!Dropbox.com\Dropbox (Personal)\sync_output", type=str)

    parser.add_argument("--configfile", type=str, required=True)
    parser.add_argument("--size", '-s', default=2048, type=int)
    parser.add_argument("--quality", '-q', default=55, type=int)
    parser.add_argument("--dryrun", action='store_true')

    args = parser.parse_args()

    main(logger, args)
