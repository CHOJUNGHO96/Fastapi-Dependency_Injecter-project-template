import json
import os
import platform
import re
from os import path


def decrypt_config(common_path: str) -> dict:
    """
    main_config file decrypt
    :param common_path: common path
    """
    main_config: str = path.join(common_path, "main_config.json")
    crypt_module: str = (
        path.join(common_path, "crypt_aes.exe")
        if platform.system() == "Windows"
        else path.join(common_path, "crypt_aes.so")
    )

    # main_config 파일을 복호화하여 json_data에 저장
    decrypted_string: str = os.popen(f"{crypt_module} -file={main_config} -mode=decrypt").read()
    byte_values: bytes = bytes(list(map(int, re.findall(r"\b\d+\b", decrypted_string))))
    json_data: dict = json.loads(byte_values.decode("utf-8"))

    return json_data
