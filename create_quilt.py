import re
import math
from pathlib import Path
from PIL import Image


def glob_files(reverse: bool = True) -> dict[str, list[tuple[int, Path]]]:
    img_dir = Path("./input/")
    img_file_paths = list(img_dir.glob("*.*g"))
    categorize_regex = re.compile(r"(\D*)([0-9]+).*\.(.+)")
    img_file_dict: dict[str, list[tuple[int, Path]]] = {}
    for file in img_file_paths:
        match_obj = categorize_regex.fullmatch(file.name)
        if match_obj is None:
            continue
        prefix = match_obj.group(1) if len(match_obj.group(1)) > 0 else ""
        extension = match_obj.group(3)
        key = f"{prefix}_{extension}" if len(prefix) > 0 else f"none_{extension}"
        if key not in img_file_dict:
            img_file_dict[key] = []
        number = int(match_obj.group(2), 10)
        img_file_dict[key].append((number, file))
    for value in img_file_dict.values():
        value.sort(key=lambda v: v[0], reverse=reverse)
    return img_file_dict


def calc_max_divisor(num: int) -> tuple[int, int]:
    if num <= 0 or (num != int(num)):
        raise ValueError("Number must be natural number.")
    i_sqrt = 1 + math.isqrt(num - 1)
    for i in range(i_sqrt, 1, -1):
        if num % i == 0:
            return (i, int(num / i))
    return (1, num)


def create_quilt(img_files: list[Path]) -> tuple[Image.Image, int, int, float]:
    if len(img_files) == 0:
        raise ValueError("empty image file list.")
    test_image = Image.open(img_files[0])
    orig_width = test_image.size[0]
    orig_height = test_image.size[1]
    print(f"{img_files[0].name}: {orig_width}px x {orig_height}px")
    del test_image
    size = len(img_files)
    (row_size, column_size) = calc_max_divisor(size)
    result_width = orig_width * column_size
    result_height = orig_height * row_size
    print(f"-> {result_width}px x {result_height}px ({row_size}x{column_size})")
    result_image = Image.new("RGB", (result_width, result_height))
    for i, file in enumerate(img_files):
        img_row = i // column_size
        img_column = i % column_size
        img_y = ((row_size - 1) - img_row) * orig_height
        img_x = img_column * orig_width
        img = Image.open(file)
        # print(f"paste -> {img_x}({img_column}), {img_y}({img_row})")
        result_image.paste(img, (img_x, img_y))
        del img
    print("concat.")
    return (result_image, column_size, row_size, (orig_width / orig_height))


def main():
    images_name = glob_files()
    quilts = {k: create_quilt([p[1] for p in v]) for (k, v) in images_name.items()}
    for (prefix, quilt) in quilts.items():
        out_prefix = f"{prefix}_" if prefix != "" else ""
        out_filename = (
            f"./output/{out_prefix}quilt_qs{quilt[1]}x{quilt[2]}a{quilt[3]}.png"
        )
        print(f"Save quilt: {out_filename}")
        quilt[0].save(out_filename)


if __name__ == "__main__":
    main()
