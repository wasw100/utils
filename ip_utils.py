# -*- coding: utf-8 -*-
import random

def ip_to_num(ip):
    """Takes an IP string and returns its decimal equivalent"""
    octects = ip.split(".")
    if len(octects) == 4:
        num = sum([int(octects[i]) << ((3-i)*8) for i in range(0,4)])
        if num < 0 or num > 0xFFFFFFFF:
            return None
        else:
            return num
    else:
        return None


def num_to_ip(num):
    """Takes an decimal representation of an IP and converts to a string"""
    if num < 0 or num > 0xFFFFFFFF:
        return None
    else:
        return ".".join([str((num >> ((3-i)*8)) & 0xFF) for i in range(0, 4)])


def random_ip():
    """generate a random ip"""
    num = random.randint(0, 0xFFFFFFFF)
    return num_to_ip(num)


if __name__ == '__main__':
    print random_ip()
