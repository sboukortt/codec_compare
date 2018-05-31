# codec_compare

A small framework for comparing metrics for still image codecs. The framework is portable, and runs inside a Docker container. The `Dockerfile` includes 4 anchor codecs (`jpeg`, `kakadu`, `webp`, `hevc`) and encoding/decoding scripts for each codec. By default, the framework encodes 8 BPP targets per encoder (`0.06, 0.12`, `0.25`, `0.50`, `0.75`, `1.00`, `1.50`, `2.00`) and two colorspaces (`RGB` and `YUV420`). The encode and decode for each codec is handled by small scripts placed in the `./encode` and `./decode` directories. The anchor codec scripts are written in Python, but you could use any language you'd like. Each script is called by the framework with the following command-line arguments:

#### Encode args:
```py
image_src  = sys.argv[1]
image_out  = sys.argv[2]
bpp_target = sys.argv[3]
width      = sys.argv[4]
height     = sys.argv[5]
pix_fmt    = sys.argv[6] #either yuv420p or ppm
depth      = sys.argv[7] 
```

#### Decode args:
```py
image_src  = sys.argv[1]
image_out  = sys.argv[2]
width      = sys.argv[3]
height     = sys.argv[4]
pix_fmt    = sys.argv[5] #either yuv420p or ppm 
```

#### Source images:
Place your source images in `./images_classes/class<X>_<bitdepth>bit/` for classes A and B,
Example: `./images_classes/classA_8bit/`.

Place your source images in `./images_classes/class<X>/` for classes C, D and E.
Example: `./images_classes/classC/`.

#### To add another codec:
Update the `Dockerfile` to include your binaries.
Add an encode and decode script in `./encode` and `./decode`.

#### To build container:
`docker build -t codec_compare .`

#### To run container:
`docker run -it -v $(pwd):/codec_compare codec_compare`

#### To encode, decode, calculate metrics:
`./compare.py <path to images folder>/`
Example: `./compare.py images_classes/classA_8bit/`

#### Notes from PINAR:
If you want to exclude a codec, remove the <codecname>.py file from both `./encode` and `./decode` folders.

If you remove hevc.py from both folders, then you can use compare_pinar_hevc.py for *HEVC encoding & decoding only*.

For this, after removing the encoding and decoding files, place them into new folders called `./encode_hevc`, `./decode_hevc` respectively. Also create new directories `./output_hevc` and `./metrics_hevc`.

Then use the command line: 
`./compare_pinar_hevc.py <path to image>`
Example: `./compare_pinar_hevc.py images_classes/classA_8bit/bike3.ppm`

If you want to use HEVC for an entire class of images (a folder), you can use the `hevc_commands.py`:
Example: `hevc_commands.py images_classes/classC` will generate a text file called `classC_commands.txt`.

You can parallelilze each line of command in this text file as such:
`parallel -k -j <number of cores you have> < classC_commands.txt`

If you don't have parallel, install it first:
`apt-get install parallel`

And that's all :) 

#### To generate graphs:
`./visualize.py ./metrics/*.json`
