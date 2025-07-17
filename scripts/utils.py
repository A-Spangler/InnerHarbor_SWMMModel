# By: Ava Spangler
# Date: 7/16/25
# Description: This code has utility functions, like one to clean utf-8 encoding that pcswmm messes up sometimes.
from config import rpts
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

    # Replace known byte issues (e.g. superscript 3)
    content = content.replace(b'\xc2\xb3', b'3')  # superscript 3

    # Now decode, replacing any remaining invalid bytes in the text
    decoded = content.decode('utf-8', errors='replace')

    output_path = rpt_path if inplace else rpt_path.replace('.rpt', '_cleaned.rpt')
    with open(output_path, 'w', encoding='utf-8') as f:  # TEXT MODE, not 'wb'
        f.write(decoded)  # decoded is a str
    return output_path