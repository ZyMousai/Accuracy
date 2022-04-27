from binascii import b2a_hex, a2b_hex
from config import MysqlConfig, globals_config
from Crypto.Cipher import AES
import hashlib

# 如果text不足16位的倍数就用空格补足为16位
PASSWORD_KEY_BYTE = globals_config.PASSWORD_KEY.encode()
IV_BYTE = globals_config.IV.encode()


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    mode = AES.MODE_CBC
    text = add_to_16(text)
    cryptos = AES.new(PASSWORD_KEY_BYTE, mode, IV_BYTE)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text).decode()


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    mode = AES.MODE_CBC
    cryptos = AES.new(PASSWORD_KEY_BYTE, mode, IV_BYTE)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


def sha1_encode(text):
    sha1 = hashlib.sha1()
    sha1.update(text.encode('utf-8'))
    return sha1.hexdigest()
