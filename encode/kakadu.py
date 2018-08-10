#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

image_src  = sys.argv[1]
image_out  = sys.argv[2]
bpp_target = sys.argv[3]
width      = sys.argv[4]
height     = sys.argv[5]
pix_fmt    = sys.argv[6]
depth      = sys.argv[7]

if pix_fmt == "ppm" or pix_fmt == 'pgm' or pix_fmt == 'tif':
    kakadu_bin = '/tools/kakadu/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827/kdu_compress'
    cmd = [kakadu_bin, "-i", image_src, "-o", image_out, "-rate", bpp_target]
elif pix_fmt == 'pfm':
    kakadu_bin = '/tools/kakadu/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827/kdu_compress'
    cmd = [kakadu_bin, "-i", image_src, "-o", image_out, "-rate", bpp_target, "-fprec", "32F8"]
elif pix_fmt == "yuv420p":
    in_tmp = '/tmp/kakadu_%sx%s_%sb_420.yuv' % (width, height, depth)
    shutil.copyfile(image_src, in_tmp)
    out_tmp = '/tmp/kakadu.mj2'
    kakadu_bin = '/tools/kakadu/KDU7A2_Demo_Apps_for_Ubuntu-x86-64_170827/kdu_v_compress'
    cmd = [kakadu_bin, "-i", in_tmp, "-o", out_tmp, "-rate", bpp_target, "-precise", "-tolerance", "0"]

print " ".join(cmd)
try:
    output = subprocess.check_output(cmd)
    if pix_fmt == "yuv420p":
        shutil.copyfile(out_tmp, image_out)
except subprocess.CalledProcessError as e:
    print e.output
    sys.exit(1)

print output

