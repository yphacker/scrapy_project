# coding=utf-8
# author=yphacker

import base64


def get_image_url(img_hash):
    return decode_base64(img_hash)[2:]


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data)


if __name__ == '__main__':
    s = 'Ly93eDQuc2luYWltZy5jbi9tdzYwMC8wMDc2QlNTNWx5MWZ3amhrMGJvb3NqMzFpMDIwMG5lei5qcGc='
    print(decode_base64(s).decode('utf8'))
