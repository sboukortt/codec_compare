#!/usr/bin/env python
import os
import argparse

parser = argparse.ArgumentParser(description='codec_compare')
parser.add_argument('path', metavar='DIR',
                    help='path to image directory')
args = parser.parse_args()
classpath = args.path
classname = classpath.split('/')[1]

commandfilename = '%s_commands.txt' % classname
commandfile = open(commandfilename, 'w')

for filename in os.listdir(classpath):
    command = './compare_pinar_hevc.py %s%s |& tee %s_hevc_output.log' % (classpath, filename, filename)
    commandfile.write(str(command) + '\n')
