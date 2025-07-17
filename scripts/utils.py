# By: Ava Spangler
# Date: 7/16/25
# Description: This code has utility functions, like one to clean utf-8 encoding that pcswmm messes up sometimes.

import os

def clean_rpt_encoding(rpt_path, inplace=True):
    """
    Cleans a SWMM .rpt file by replacing byte 0xb3 (superscript 3) with ASCII '3'.
    By default modifies file in-place; if inplace=False, appends '_cleaned' to filename.
    """
    if not os.path.isfile(rpt_path):
        raise FileNotFoundError(f"File not found: {rpt_path}")

    with open(rpt_path, 'rb') as f:
        content = f.read()

    clean_content = content.replace(b'\xb3', b'3')

    output_path = rpt_path if inplace else rpt_path.replace('.rpt', '_cleaned.rpt')
    with open(output_path, 'wb') as f:
        f.write(clean_content)
    return output_path

