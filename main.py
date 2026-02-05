import pymupdf
from datetime import datetime
import re
import shutil
import os
import argparse
import math


parser = argparse.ArgumentParser(
    description="Process a file with optional flags"
)

# filepath arg
parser.add_argument(
    "file",
    help="File to process"
)

#watermark flag
parser.add_argument(
    "--watermark",
    action="store_true",
    help="Watermark the source file after sorting"
)

args = parser.parse_args()

doc = pymupdf.open(str(args.file))

codes_dict = {}
all_codes = []

for page in doc:
    for annot in page.annots() or []:
        if annot.info["content"] not in codes_dict:
            codes_dict[annot.info["content"]] = [page.number]
        else:
            codes_dict[annot.info["content"]].append(page.number)
            
        all_codes.append(annot.info["content"])

unique_codes = list(set(all_codes))
filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".pdf"

for i in range(len(unique_codes)):
    if not os.path.isdir(unique_codes[i]):
        os.mkdir(unique_codes[i])

for i in range(len(codes_dict)):
    dst = pymupdf.open()
    for p in codes_dict[unique_codes[i]]:
        dst.insert_pdf(doc, from_page=p, to_page=p)
        new_page = dst[-1]
        for annot in new_page.annots() or []:
            detected_rotation = annot.rotation
        
        final_rotation = (new_page.rotation + detected_rotation) % 360
        new_page.set_rotation(final_rotation)
    dst.save(filename)
    dst.close()
    dstfolder = str(unique_codes[i]) + "/" + str(filename)
    shutil.move(filename, dstfolder)

doc.close()

def add_rotated_text_watermark(input_pdf, watermark_text):
    doc = pymupdf.open(input_pdf)

    for page_num in range(doc.page_count):
        page = doc[page_num]
        
#         rect = page.rect
#         if rect.width > rect.height:
#             page.set_rotation((page.rotation + 90) % 360)

        # choose desired font
        font = pymupdf.Font("tiro")
        page.insert_font(fontname="myfont", fontbuffer=font.buffer)
        font_size = 100

        # choose 2 points to define a line along which to insert text
        p1 = pymupdf.Point(300, 400)
        p2 = pymupdf.Point(400, 300)
        # compute angle of line
        cos, sin = (p2 - p1).unit
        theta = math.degrees(math.atan2(sin, cos))
        # define matrix to rotate text
        mat = pymupdf.Matrix(-theta)
        # we want to insert this text along the line
        text = watermark_text #f"This text inserted at {round(-theta,1)}°"
        """
        Optional: Shrink / stretch text to fit along the line
        ---------------------------------------------------------------------
        """
        # length of line
        line_len = abs(p2 - p1)
        text_len = font.text_length(text, fontsize=font_size)
        # scale factor
        scale = line_len / text_len
        # scale matrix
        scale_mat = pymupdf.Matrix(scale, scale)
#         mat *= scale_mat  # (un-)comment to see its effect
        """
        ---------------------------------------------------------------------
        """
        page.insert_text(
            p1,
            text,
            fontsize=font_size,
            fontname="myfont",
            fill_opacity=0.3,
            stroke_opacity=0.3,
            color=(0.7, 0.7, 0.7),
            fill=(1, 1, 1),
            border_width=0.02,
            render_mode=2,
            morph=(p1, mat),
        )

    doc.saveIncr()
    doc.close()

if args.watermark:
    add_rotated_text_watermark(args.file, "SORTED")

print("Done!")

