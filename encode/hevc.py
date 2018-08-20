#!/usr/bin/env python
import sys
import os
import subprocess
import math

image_src  = sys.argv[1]
image_out  = sys.argv[2]
bpp_target = sys.argv[3]
width      = sys.argv[4]
height     = sys.argv[5]
pix_fmt    = sys.argv[6]
depth      = sys.argv[7]

hevc_bin = '/tools/HM-16.18+SCM-8.7/bin/TAppEncoderHighBitDepthStatic'
if depth == '12' or depth == '16' or depth == '32' or pix_fmt == 'pgm':
    hevc_cfg = '/tools/HM-16.18+SCM-8.7/cfg/encoder_intra_main_rext.cfg'
else:
    hevc_cfg = '/tools/HM-16.18+SCM-8.7/cfg/encoder_intra_main_scc.cfg'

HDRConvert_dir = '/tools/HDRTools-0.18-dev/bin/HDRConvert'
ppm_to_rgb_cfg = 'convert_configs/HDRConvertPPMToRGB444fr.cfg'
pgm_to_yuv_cfg = 'convert_configs/HDRConvertPGM8ToYCbCr400fr8.cfg'

rgb_dest = '/tmp/tmp.rgb'
yuv_dest = '/tmp/tmp.yuv'
img_src_orig = image_src

if 'classE' in image_src:
    primary = '1'
else:
    primary = '0'

if pix_fmt == "ppm" or pix_fmt == 'pfm':
    chroma_fmt = "444"
    if 'HOTEL' in image_src or 'CATS' in image_src or 'AERIAL2' in image_src or 'TEXTURE' in image_src or 'GOLD' in image_src or 'XRAY' in image_src:
        try:
            cmd = ["ffmpeg", "-y", "-i", image_src, "-pix_fmt", "gbrp", rgb_dest]
            output = subprocess.check_output(cmd)
            image_src = rgb_dest
        except subprocess.CalledProcessError as e:
            print cmd
            print e.output
            sys.exit(1)
    else:
        try:
            cmd = [HDRConvert_dir, '-f', ppm_to_rgb_cfg, '-p', 'SourceFile=%s' % image_src, '-p', 'SourceWidth=%s' % width,
                   '-p', 'SourceHeight=%s' % height, '-p', 'SourceBitDepthCmp0=%s' % depth, '-p', 'SourceBitDepthCmp1=%s'
                   % depth, '-p', 'SourceBitDepthCmp2=%s' % depth, '-p', 'SourceColorPrimaries=%s' % primary, '-p',
                   'OutputFile=%s' % rgb_dest, '-p', 'OutputWidth=%s' % width, '-p', 'OutputHeight=%s' % height, '-p',
                   'OutputBitDepthCmp0=%s' % depth, '-p', 'OutputBitDepthCmp1=%s' % depth, '-p', 'OutputBitDepthCmp2=%s'
                   % depth, '-p', 'OutputColorPrimaries=%s' % primary]
            output = subprocess.check_output(cmd)
            image_src = rgb_dest
        except subprocess.CalledProcessError as e:
            print cmd
            print e.output
            sys.exit(1)

elif pix_fmt == 'pgm':
    chroma_fmt = "400"
    try:
        cmd = [HDRConvert_dir, '-f', pgm_to_yuv_cfg, '-p', 'SourceFile=%s' % image_src, '-p', 'SourceWidth=%s' % width,
               '-p', 'SourceHeight=%s' % height, '-p', 'SourceBitDepthCmp0=%s' % depth, '-p', 'SourceBitDepthCmp1=%s'
               % depth, '-p', 'SourceBitDepthCmp2=%s' % depth, '-p', 'SourceColorPrimaries=%s' % primary, '-p',
               'OutputFile=%s' % yuv_dest, '-p', 'OutputWidth=%s' % width, '-p', 'OutputHeight=%s' % height, '-p',
               'OutputBitDepthCmp0=%s' % depth, '-p', 'OutputBitDepthCmp1=%s' % depth, '-p', 'OutputBitDepthCmp2=%s'
               % depth, '-p', 'OutputColorPrimaries=%s' % primary]
        output = subprocess.check_output(cmd)
        image_src = yuv_dest
    except subprocess.CalledProcessError as e:
        print cmd
        print e.output
        sys.exit(1)
elif pix_fmt == "yuv444p":
    chroma_fmt = "444"
elif pix_fmt == "yuv422p":
    chroma_fmt = "422"
elif pix_fmt == "yuv420p":
    chroma_fmt = "420"
elif pix_fmt == "rgb":
    chroma_fmt = "444"

qp_min, qp_max = 0, 51
qp = qp_max / 2
step = qp / 2

for i in range(0, int(math.floor(math.log(qp_max)/math.log(2)))):
    if pix_fmt == "ppm":
        if 'XRAY' in img_src_orig:
            cmd = [hevc_bin, "-c", hevc_cfg, "-f", "1", "-fr", "1", "-q", str(qp), "-wdt", width, "-hgt", height,
                   "--InputChromaFormat=%s" % (chroma_fmt), "--InternalBitDepth=%s" % (depth),
                   "--ConformanceWindowMode=1", "--InputColourSpaceConvert=RGBtoGBR", "-i", image_src, "-b", image_out, "-o", "/dev/null"
                   ]
        else:
            cmd = [hevc_bin, "-c", hevc_cfg, "-f", "1", "-fr", "1", "-q", str(qp), "-wdt", width, "-hgt", height,
                   "--InputChromaFormat=%s" % (chroma_fmt), "--InternalBitDepth=%s" % (depth), "--InputBitDepth=%s" % (depth), "--OutputBitDepth=%s" % (depth),
                   "--ConformanceWindowMode=1", "--InputColourSpaceConvert=RGBtoGBR", "-i", image_src, "-b", image_out, "-o", "/dev/null"
                   ]
    else:
        cmd = [hevc_bin, "-c", hevc_cfg, "-f", "1", "-fr", "1", "-q", str(qp), "-wdt", width, "-hgt", height,
               "--InputChromaFormat=%s" % (chroma_fmt), "--InternalBitDepth=%s" % (depth), "--InputBitDepth=%s" % (depth), "--OutputBitDepth=%s" % (depth),
               "--ConformanceWindowMode=1", "-i", image_src, "-b", image_out, "-o", "/dev/null"
               ]
    print " ".join(cmd)
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print e.output
        sys.exit(1)

    size = os.path.getsize(image_out) * 8
    bpp  = float(size) / float((int(width) * int(height)))
    print qp, step, size, bpp, bpp_target

    qp += step * (1 if (bpp > float(bpp_target)) else -1)
    step /= 2

print output
