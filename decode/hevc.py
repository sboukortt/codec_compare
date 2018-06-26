#!/usr/bin/env python
import sys
import os
import subprocess

img_enc = sys.argv[1]
img_dec = sys.argv[2]
width   = sys.argv[3]
height  = sys.argv[4]
pix_fmt = sys.argv[5]
depth   = sys.argv[6]

hevc_bin = '/tools/HM-16.18+SCM-8.7/bin/TAppDecoderStatic'
tmp_dec  = '/tmp/tmp.rgb'

if pix_fmt == "ppm":
    out = tmp_dec
else:
    out = img_dec

try:
    cmd = [hevc_bin, "-b", img_enc, "-d", depth, "-o", out]
    print " ".join(cmd)
    output = subprocess.check_output(cmd)
except subprocess.CalledProcessError as e:
    print " ".join(cmd), e.output
    sys.exit(1)

if pix_fmt == "ppm":
    try:
        if depth == '8':
            cmd = ["ffmpeg", "-y", "-pix_fmt", "gbrp", "-s:v", width + "x" + height, "-i", tmp_dec, "-vframes", "1", img_dec]
        else:
            cmd = ["ffmpeg", "-y", "-pix_fmt", "gbrp"+depth+"le", "-s:v", width + "x" + height, "-i", tmp_dec, "-vframes", "1", img_dec]
        print " ".join(cmd)
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print " ".join(cmd), e.output
        sys.exit(1)
