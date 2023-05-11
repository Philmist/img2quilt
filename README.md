# Create a quilt image from ordered numbered images.

## Usage

Copy the numbered image files into the folder.
The file name must contain a number.

```
000001.jpg
000002.jpg
000003.jpg
...
```

```
foobar0001.jpg
foobar0002.jpg
...
```

Then, create and activate virtual enviroment (venv),
install dependency from `requirements.txt`.

Run `create_quilt.py`.

Quilt images saved in `./output/`.

You may need to modify `create_quilt.py` because of order of images (default: Right to Left). See `glob_files` function.

## Tips

Ordered numbered images can be created with ffmpeg.

```
ffmpeg -ss [from timestamp] -to [to timestamp] -i [source movie file] -qmin 1 -q:v 1 %06d.jpg
```

## LICENSE

MIT
