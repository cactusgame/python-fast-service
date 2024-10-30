import os
import contextlib
from os import stat
from itertools import cycle
from datetime import timedelta, datetime
import pyAesCrypt
import hashlib
import io

from ab.utils.exceptions import AlgorithmException

bufferSizeDef = 64 * 1024


def license_impl(create, days, verify):
    if create is not None:
        license_create(create, days)
    if verify is not None:
        license_verify(verify)


# only enc
def step1(input_line):
    sout = [chr(ord(a) ^ ord(b)) for (a, b) in
            zip(input_line, cycle("utf-8" + "utf-8"))]
    return "".join(sout)


# enc + md5
def step2(input_line):
    m = hashlib.md5()
    m.update(step1(input_line).encode('utf-8'))
    return m.hexdigest()


def license_create(path, days):
    """
        许可证明文格式
        ===== license start =====
        to:2022-06-19
        inode filename1
        inode filename2
        inode filename3
        inode filename4
        inode filename5
        inode filename6
        inode filename7
        ===== license end =====
    :param path:
    :return:
        """

    result = ""
    with open("license.ab", 'w') as of:
        # start
        l = "===== license start =====\n"
        of.write(l)
        result = result + l

        # enddate
        enddate = datetime.strftime(datetime.today() + timedelta(days=int(days)), '%Y-%m-%d')
        t = "to:{}".format(enddate)
        l = step1(t)
        l = l + "\n"
        of.write(l)
        result = result + l

        with open(path) as f:
            for num, line in enumerate(f, 1):
                # only need if the num from [2,8], total 7 lines
                if 2 <= num <= 8:
                    if "---" not in line:
                        license_string = step2(line.strip())
                        of.write(license_string)
                        of.write("\n")

                        result = result + license_string + "\n"
                    else:
                        raise RuntimeError("errors in license format")

        l = "===== license end ====="
        of.write(l)
        result = result + l
    print(result)


def license_verify(license_file_path):
    import subprocess
    commands = [
        "ls -i /etc/stub0",
        "ls -i /etc/stub1",
        "ls -i /etc/stub2",
        "ls -i /etc/stub3",
        "ls -i /etc/timezone",
        "ls -i /etc/hostname",
        "ls -i /etc/locale.conf",
    ]
    # voter
    true_count = 0
    false_count = 0
    with open(license_file_path, "r") as inf:
        for num, line in enumerate(inf, 1):
            # verify date
            if num == 2:
                enddate = step1(line.strip())[3:]
                today = datetime.today().strftime("%Y-%m-%d")

                if today > enddate:
                    raise RuntimeError("license.ab expired")
            # verify checksum
            elif 3 <= num <= 9:
                ret = subprocess.run(commands[num - 3], shell=True, stdout=subprocess.PIPE, encoding="utf-8").stdout
                if step2(ret.strip()) == line.strip():
                    true_count = true_count + 1
                else:
                    false_count = false_count + 1
            else:
                pass
    if true_count < false_count:
        raise RuntimeError("invalid license.ab")


# 加密文件扩展名
SEC_FILE_POSTFIX = ".sec"


def read_text(infile, encode="UTF-8"):
    """
        纯文本解密工具
    :param infile:
    :param passw_fun():
    :param encode:
    :return:
        """

    string = ""
    with open_text(infile, encode) as text:
        for t in text:
            string = string + t
    return string


def read_json(infile, encode="UTF-8"):
    """
        json解密工具
    :param infile:
    :param passw_fun():
    :param encode:
    :return:
        """
    text = read_text(infile, encode)
    import json

    return json.loads(text)


def read_pickle(infile):
    """
        pickle解密工具
        """
    import pickle

    with open_binary(infile) as buffer:
        obj = pickle.loads(buffer)
        return obj


@contextlib.contextmanager
def open_text(infile, encode="utf-8"):
    """
        返回解压后的文本流
    :param infile:
    :param passw_fun():
    :param encode:
    :return:
        """
    if os.path.exists(infile):
        f = open(infile, "r", encoding=encode)
        yield f
        f.close()
    else:
        sec_file_path = infile + SEC_FILE_POSTFIX
        if os.path.exists(sec_file_path):
            byte_io = decrypt_to_memory(sec_file_path)
            text_obj = byte_io.getvalue().decode(encode)
            string_io = io.StringIO(text_obj)
            yield string_io
            byte_io.close()
            string_io.close()
        else:
            raise AlgorithmException(5002,sec_file_path)


@contextlib.contextmanager
def open_binary(infile):
    """
        返回解压后的二进制流
    :param infile:
    :param passw_fun():
    :param encode:
    :return:
        """
    if os.path.exists(infile):
        f = open(infile, "rb")
        max_bytes = 2 ** 31 - 1
        bytes_in = bytearray(0)
        input_size = os.path.getsize(infile)
        if input_size > max_bytes:
            raise AlgorithmException(5003,infile)
        with open(infile, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        yield bytes_in
        f.close()
    else:
        sec_file_path = infile + SEC_FILE_POSTFIX
        if os.path.exists(sec_file_path):
            byte_io = decrypt_to_memory(sec_file_path)
            yield byte_io.getvalue()
            byte_io.close()
        else:
            raise AlgorithmException(5002,sec_file_path)


def decrypt_to_memory(infile):
    """
        将加密文件解密并读取到内存ByteIO
    :param infile:
    :param passw_fun():
    :param bufferSize:
    :return:
        """
    try:
        with open(infile, "rb") as fIn:
            try:
                fOut = io.BytesIO()
                inputFileSize = stat(infile).st_size
                try:
                    # decrypt file stream
                    decryptStream(fIn, fOut, inputFileSize)
                    return fOut
                except ValueError as exd:
                    # should not remove output file here because it is still in use
                    # re-raise exception
                    raise ValueError(str(exd))
            except IOError:
                raise ValueError("Unable to write output file.")
            except ValueError as exd:
                # remove output file on error
                # re-raise exception
                raise ValueError(str(exd))

    except IOError:
        raise ValueError("Unable to read input file.")


def encryptFile(infile, outfile):
    pass


def encryptStream(fIn, fOut):
    pass


def decryptStream(fIn, fOut, inputLength):
    pass


# ========= I am a line ==============


def encrypt_file():
    return "hello world"


def encrypt_stream():
    pass


def encrypt_file2():
    pass


def encrypt_file3():
    pass


def encrypt_file4():
    pass


def add(a="", b=""):
    return a + b


def sub(a="", b=""):
    pass


def mul(a="", b=""):
    pass



def div(a="", b=""):
    pass

