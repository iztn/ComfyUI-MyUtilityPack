import os
import sys
import numpy as np
import torch

class MySEGSOrderedFilter:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                        "image": ("IMAGE",),
                        "segs": ("SEGS", ),
                        "target": (["area(=w*h)", "width", "height", "x1", "y1", "x2", "y2", "center"],),
                        "order": ("BOOLEAN", {"default": True, "label_on": "descending", "label_off": "ascending"}),
                        "take_start": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                        "take_count": ("INT", {"default": 1, "min": 0, "max": sys.maxsize, "step": 1}),
                     },
                }

    RETURN_TYPES = ("SEGS", "SEGS",)
    RETURN_NAMES = ("filtered_SEGS", "remained_SEGS",)
    FUNCTION = "doit"

    CATEGORY = "MyUtilityPack/Util"

    def doit(self, image, segs, target, order, take_start, take_count):
        segs_with_order = []

        for seg in segs[1]:
            x1 = seg.crop_region[0]
            y1 = seg.crop_region[1]
            x2 = seg.crop_region[2]
            y2 = seg.crop_region[3]

            if target == "area(=w*h)":
                value = (y2 - y1) * (x2 - x1)
            elif target == "width":
                value = x2 - x1
            elif target == "height":
                value = y2 - y1
            elif target == "x1":
                value = x1
            elif target == "x2":
                value = x2
            elif target == "y1":
                value = y1
            elif target == "center":
                image_height, image_width = image.shape[1], image.shape[2]
                value = -(abs((x1 + x2) / 2 - image_width / 2) + abs((y1 + y2) / 2 - image_height / 2))
            else:
                value = y2

            segs_with_order.append((value, seg))

        if order:
            sorted_list = sorted(segs_with_order, key=lambda x: x[0], reverse=True)
        else:
            sorted_list = sorted(segs_with_order, key=lambda x: x[0], reverse=False)

        result_list = []
        remained_list = []

        for i, item in enumerate(sorted_list):
            if take_start <= i < take_start + take_count:
                result_list.append(item[1])
            else:
                remained_list.append(item[1])

        return ((segs[0], result_list), (segs[0], remained_list), )
