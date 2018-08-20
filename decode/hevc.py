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

hevc_bin = '/tools/HM-16.18+SCM-8.7/bin/TAppDecoderHighBitDepthStatic'
tmp_dec  = '/tmp/tmp.rgb'
tmp_dec_yuv = '/tmp/tmp.yuv'

if pix_fmt == "ppm":
    out = tmp_dec
elif pix_fmt == 'pgm':
    out = tmp_dec_yuv
else:
    out = img_dec

try:
    if pix_fmt == 'ppm':
        if 'XRAY' in img_enc:
            cmd = [hevc_bin, "-b", img_enc, "-d", '8', "-o", out]
        else:
            cmd = [hevc_bin, "--OutputColourSpaceConvert=GBRtoRGB", "-b", img_enc, "-d", depth, "-o", out]
    else:
        cmd = [hevc_bin, "-b", img_enc, "-d", depth, "-o", out]
    print " ".join(cmd)
    output = subprocess.check_output(cmd)
except subprocess.CalledProcessError as e:
    print " ".join(cmd), e.output
    sys.exit(1)

HDRConvert_dir = '/tools/HDRTools-0.18-dev/bin/HDRConvert'
rgb_to_ppm_cfg = 'convert_configs/HDRConvertRGB444frToPPM.cfg'

if 'classE' in img_enc:
    primary = '1'
else:
    primary = '0'

if pix_fmt == "ppm":
    try:
        if 'XRAY' in img_enc:
            cmd = ["ffmpeg", "-y", "-pix_fmt", "gbrp", "-s:v", width + "x" + height, "-i", tmp_dec, "-vframes", "1", img_dec]
        else:
            cmd = [HDRConvert_dir, '-f', rgb_to_ppm_cfg, '-p', 'SourceFile=%s' % out, '-p', 'SourceWidth=%s' % width,
                   '-p', 'SourceHeight=%s' % height, '-p', 'SourceBitDepthCmp0=%s' % depth, '-p', 'SourceBitDepthCmp1=%s'
                   % depth, '-p', 'SourceBitDepthCmp2=%s' % depth, '-p', 'SourceColorPrimaries=%s' % primary, '-p',
                   'OutputFile=%s' % img_dec, '-p', 'OutputWidth=%s' % width, '-p', 'OutputHeight=%s' % height, '-p',
                   'OutputBitDepthCmp0=%s' % depth, '-p', 'OutputBitDepthCmp1=%s' % depth, '-p', 'OutputBitDepthCmp2=%s'
                   % depth, '-p', 'OutputColorPrimaries=%s' % primary]
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print " ".join(cmd), e.output
        sys.exit(1)

if pix_fmt == "pgm":
    try:
        cmd = ['cp', out, img_dec]
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print " ".join(cmd), e.output
        sys.exit(1)
