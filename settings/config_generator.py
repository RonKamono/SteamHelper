import os


class ConfigGenerator:
    user = os.getenv("USERPROFILE")
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&*+-=?@^_'
    digits = '01234567890'
