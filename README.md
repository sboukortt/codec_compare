# codec_compare

A small framework for comparing metrics for still image codecs. The framework is portable, and runs inside a Docker container. The `Dockerfile` includes 4 anchor codecs (`jpeg`, `kakadu`, `webp`, `hevc`) and encoding/decoding scripts for each codec. By default, the framework encodes 8 BPP targets per encoder (`0.06, 0.12`, `0.25`, `0.50`, `0.75`, `1.00`, `1.50`, `2.00`) and two colorspaces (`RGB` and `YUV420`). The encode and decode for each codec is handled by small scripts placed in the `./encode` and `./decode` directories. The anchor codec scripts are written in Python, but you could use any language you'd like. Each script is called by the framework with the following command-line arguments:

#### Encode args:
```py
image_src  = sys.argv[1]
image_out  = sys.argv[2]
bpp_target = sys.argv[3]
width      = sys.argv[4]
height     = sys.argv[5]
pix_fmt    = sys.argv[6] 
depth      = sys.argv[7] 
```

#### Decode args:
```py
image_src  = sys.argv[1]
image_out  = sys.argv[2]
width      = sys.argv[3]
height     = sys.argv[4]
pix_fmt    = sys.argv[5] 
depth      = sys.argv[6]
```

#### Source images:
Place your source images in `./images_classes/class<X>_<bitdepth>bit/` for classes A and B,
Example: `./images_classes/classA_8bit/`.
Note: .yuv files in class A 10 bit cannot be handled in this version!

Place your source images in `./images_classes/class<X>/` for classes C, D and E.
Example: `./images_classes/classC/`.

Place your source images in `./images_classes/classE_exr/` for class E images in .exr format

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

If you are going to encode and decode images with bit depth greater than 10bpp, after building the container you have to enable RExt__HIGH_BIT_DEPTH_SUPPORT. Here's how:

After you build and run the container, type the following commands:

apt-get update

apt-get install vim

Y

vi /tools/HM-16.18+SCM-8.7/source/Lib/TLibCommon/TypeDef.h


In line 132 you have #define RExt__HIGH_BIT_DEPTH_SUPPORT set to 0. You need to change this to 1, save and quit (press i to switch to insert mode, when you finish changes press ESC to exit insert mode, then type :wq and hit ENTER. Then build HM again.

Now you won't have problems.

And that's all :) 

#### To generate graphs:
`./visualize.py ./metrics/*.json`
