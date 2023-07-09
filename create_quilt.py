import re
import math
import logging
from typing import Literal
from pathlib import Path
from dataclasses import dataclass
from PIL import Image
import yaml


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


@dataclass
class QuiltConf:
    reverse: bool = True
    annotate_str: str | None = None
    annotate_position: Literal[
        "top-left", "top-right", "bottom-left", "bottom-right"
    ] = "bottom-right"
    font_name: str | None = None


default_conf = QuiltConf()


def glob_files(reverse: bool = True) -> dict[str, list[tuple[int, Path]]]:
    img_dir = Path("./input/")
    img_file_paths = list(img_dir.glob("*.*g"))
    categorize_regex = re.compile(r"(.*?)_?([0-9]+)\.(.+)")
    img_file_dict: dict[str, list[tuple[int, Path]]] = {}
    for file in img_file_paths:
        match_obj = categorize_regex.fullmatch(file.name)
        if match_obj is None:
            continue
        prefix = match_obj.group(1) if len(match_obj.group(1)) > 0 else ""
        extension = match_obj.group(3)
        key = f"{prefix}_{extension}" if len(prefix) > 0 else f"none_{extension}"
        if key not in img_file_dict:
            logger.info("Add key: %s", key)
            img_file_dict[key] = []
        number = int(match_obj.group(2), 10)
        img_file_dict[key].append((number, file))
    for value in img_file_dict.values():
        value.sort(key=lambda v: v[0], reverse=reverse)
    return img_file_dict


def calc_max_divisor(num: int) -> tuple[int, int]:
    """Calculate divisor for quilt(columns, rows)."""
    if num <= 0 or (num != int(num)):
        raise ValueError("Number must be natural number.")
    i_sqrt = 1 + math.isqrt(num - 1)
    for i in range(i_sqrt, 1, -1):
        if num % i == 0:
            return (i, int(num / i))
    return (1, num)


def create_quilt(img_files: list[Path]) -> tuple[Image.Image, int, int, float]:
    """Create quilt image from passed image lists.

    Create quilt image from image files.
    Image files must have same dimension.
    This function returns quilt image with aspect ratio (width / height).

    :param img_files: List of Path object for image file.
    :return: Result Image and column size, row size, original aspect ratio.
    """
    if len(img_files) == 0:
        raise ValueError("empty image file list.")
    test_image = Image.open(img_files[0])
    orig_size = (test_image.size[0], test_image.size[1])
    logging.info(
        "%s: %dpx x  %dpx",
        img_files[0].name, orig_size[0], orig_size[1]
    )
    del test_image
    (row_size, column_size) = calc_max_divisor(len(img_files))
    result_size = (orig_size[0] * column_size, orig_size[1] * row_size)
    logging.info(
        " -> %dpx x %dpx (%dx%d)",
        result_size[0], result_size[1],
        row_size, column_size
    )
    result_image = Image.new("RGB", result_size)
    for i, file in enumerate(img_files):
        img_row = i // column_size
        img_column = i % column_size
        img_y = ((row_size - 1) - img_row) * orig_size[1]
        img_x = img_column * orig_size[0]
        img = Image.open(file)
        # print(f"paste -> {img_x}({img_column}), {img_y}({img_row})")
        result_image.paste(img, (img_x, img_y))
        del img
    logging.info("concating completed.")
    return (result_image, column_size, row_size, (orig_size[0] / orig_size[1]))


def main():
    images_name = glob_files()
    for (prefix, value) in images_name.items():
        quilt = create_quilt([item[1] for item in value])
        out_prefix = f"{prefix}_" if prefix != "" else ""
        out_filename = (
            f"./output/{out_prefix}quilt_qs{quilt[1]}x{quilt[2]}a{quilt[3]}.png"
        )
        logger.info("Saving: %s", out_filename)
        quilt[0].save(out_filename)
        logger.info("Saved: %s", out_filename)
        del quilt


if __name__ == "__main__":
    main()
