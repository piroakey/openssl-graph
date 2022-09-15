#!/usr/bin/env python3
import sys
import re
import logging
import matplotlib.pyplot as plt
import seaborn as sbn
import numpy as np

FONT_FAMILY = "MS Gothic"
BAR_WIDTH = 0.8
GRAPH_NAME_FULL = "full.png"
GRAPH_NAME_RESUM = "resumption.png"
GRAPH_NAME_CRYPTO = "crypto.png"
GRAPH_NAME_KEYEX = "keyex.png"
GRAPH_NAME_SIGN = "sign.png"
GRAPH_NAME_VERIFY = "verify.png"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def handshake_graph(filenames=[], x_label="", y_label=""):

    logger.info(">>>>> handshake_graph")

    BAR_WIDTH = 0.6

    pat_hs = re.compile('^(TLS\d\.\d) full-handshake\:.+; (\d+(?:\.\d+)?) connections.*$')  # fmt: skip # noqa
    pat_re = re.compile('^(TLS\d\.\d) resumption:.+; (\d+(?:\.\d+)?) connections/user sec,.+$')  # fmt: skip # noqa

    sbn.set()
    sbn.set_style("whitegrid")
    sbn.set_palette("PRGn_r")

    hs_x = []
    re_x = []
    hs_bar = []
    re_bar = []

    for filename in filenames:
        with open(filename, "r") as f:
            for i, l in enumerate(f):
                datas = pat_hs.search(l)
                if datas:
                    label = datas.groups()[0].strip()
                    hs_x.append(label)
                    data = datas.groups()[1]
                    hs_bar.append(data)

                datas = pat_re.search(l)
                if datas:
                    label = datas.groups()[0].strip()
                    re_x.append(label)
                    data = datas.groups()[1]
                    re_bar.append(data)

                # print(label, data)

    hs_x = np.array(hs_x)
    re_x = np.array(re_x)
    hs_bar = np.array(hs_bar, np.float32)
    re_bar = np.array(re_bar, np.float32)

    logger.info(hs_x)
    logger.info(hs_bar)
    logger.info(re_x)
    logger.info(re_bar)

    x_position = np.arange(len(hs_x))

    # full handshake
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.barh(x_position, hs_bar, height=BAR_WIDTH)

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("TLSのバージョン", fontname=FONT_FAMILY)
    ax.set_xlabel("connections/sec", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(hs_x)
    ax.grid(axis="y")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_FULL)
    logger.info("--> {}".format(GRAPH_NAME_FULL))

    # resumption
    x_position = np.arange(len(re_x))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.barh(x_position, re_bar, height=BAR_WIDTH)

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("TLSのバージョン", fontname=FONT_FAMILY)
    ax.set_xlabel("connections/sec", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(re_x)
    ax.grid(axis="y")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_RESUM)
    logger.info("--> {}".format(GRAPH_NAME_RESUM))


def crypto_graph(filenames=[], x_label="", y_label=""):

    logger.info(">>>>> crypto_graph")

    pat = re.compile(
        "^([a-zA-Z0-9_-]+)\s+(\d+(?:\.\d+)?)k\s+(\d+(?:\.\d+)?)k\s+(\d+(?:\.\d+)?)k\s+(\d+(?:\.\d+)?)k\s+(\d+(?:\.\d+)?)k\s+(\d+(?:\.\d+)?)k"  # noqa
    )

    sbn.set()
    sbn.set_style("whitegrid")
    sbn.set_palette("Set1")

    x = np.array(["16 bytes", "64 bytes", "256 bytes", "1024 bytes", "8192 bytes", "16384 bytes"])

    bars = []

    for filename in filenames:
        with open(filename, "r") as f:
            for i, l in enumerate(f):
                if i < 7:
                    continue
                # print(i, l)
                datas = pat.search(l)
                label = datas.groups()[0].strip()
                bar = np.array(datas.groups()[1:], np.float64)
                # print(label, bar)
                bars.append((label, bar))

    logger.info(bars)

    x_position = np.arange(len(x))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for i, bar in enumerate(bars):
        pos = x_position - BAR_WIDTH * (1 - (2 * i + 1) / len(bars)) / 2
        ax.barh(pos, bar[1], height=BAR_WIDTH / len(bars), label=bar[0])

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("ブロックサイズ[bytes]", fontname=FONT_FAMILY)
    ax.set_xlabel("1秒あたりの処理数 [KB]", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(x)
    ax.grid(axis="y")
    ax.legend()
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_CRYPTO)
    logger.info("--> {}".format(GRAPH_NAME_CRYPTO))


def keyex_graph(filenames=[], x_label="", y_label=""):

    logger.info(">>>>> keyex_graph")

    BAR_WIDTH = 0.6

    pat = re.compile("^(.+\))\s+(\d+(?:\.\d+)?)s\s+(\d+(?:\.\d+)?)$")  # noqa

    sbn.set()
    sbn.set_style("whitegrid")
    sbn.set_palette("PRGn_r")

    x = []
    bar = []

    for filename in filenames:
        with open(filename, "r") as f:
            for i, l in enumerate(f):
                if i < 6:
                    continue
                # print(i, l)
                datas = pat.search(l)
                label = datas.groups()[0].strip().replace("(", "\n(")
                x.append(label)
                data = datas.groups()[2]
                # print(label, data)
                bar.append(data)

    x = np.array(x)
    bar = np.array(bar, np.float32)

    logger.info(x)
    logger.info(bar)

    x_position = np.arange(len(x))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.barh(x_position, bar, height=BAR_WIDTH)

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("楕円曲線の種類", fontname=FONT_FAMILY)
    ax.set_xlabel("op/s", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(x)
    ax.grid(axis="y")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_KEYEX)
    logger.info("--> {}".format(GRAPH_NAME_KEYEX))


def sign_verify_graph(filenames=[], x_label="", y_label=""):

    logger.info(">>>>> sign_verify_graph")

    BAR_WIDTH = 0.6

    pat = re.compile("^(.+\))\s+(\d+(?:\.\d+)?)s\s+(\d+(?:\.\d+)?)s\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)$")  # noqa

    sbn.set()
    sbn.set_style("whitegrid")
    sbn.set_palette("PuBu_r")

    x = []
    sign_bar = []
    verify_bar = []

    for filename in filenames:
        with open(filename, "r") as f:
            for i, l in enumerate(f):
                if i < 6:
                    continue
                if i % 2 != 0:
                    continue
                # print(i, l)
                datas = pat.search(l)
                label = datas.groups()[0].strip().replace("(", "\n(")
                x.append(label)
                sign_data = datas.groups()[3]
                sign_bar.append(sign_data)
                verify_data = datas.groups()[4]
                verify_bar.append(verify_data)

    x = np.array(x)
    sign_bar = np.array(sign_bar, np.float32)
    verify_bar = np.array(verify_bar, np.float32)

    logger.info(x)
    logger.info(sign_bar)
    logger.info(verify_bar)

    x_position = np.arange(len(x))

    # sign graph
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.barh(x_position, sign_bar, height=BAR_WIDTH)

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("楕円曲線の種類", fontname=FONT_FAMILY)
    ax.set_xlabel("sign/s", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(x)
    ax.grid(axis="y")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_SIGN)
    logger.info("--> {}".format(GRAPH_NAME_SIGN))

    # verify graph
    sbn.set_palette("PRGn")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.barh(x_position, verify_bar, height=BAR_WIDTH)

    ax.ticklabel_format(style="plain", axis="x")
    ax.set_ylabel("楕円曲線の種類", fontname=FONT_FAMILY)
    ax.set_xlabel("verify/s", fontname=FONT_FAMILY)
    ax.set_yticks(x_position)
    ax.set_yticklabels(x)
    ax.grid(axis="y")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(GRAPH_NAME_VERIFY)
    logger.info("--> {}".format(GRAPH_NAME_VERIFY))


def main():

    logger.setLevel(logging.INFO)

    if len(sys.argv) < 3:
        logger.error("openssl_graph.py crypto|keyex|sign_verify FILE_NAME1 FILE_NAME2...")
        exit(1)

    type = sys.argv[1]
    filenames = sys.argv[2:]

    if type == "handshake":
        handshake_graph(filenames)
    elif type == "crypto":
        crypto_graph(filenames)
    elif type == "keyex":
        keyex_graph(filenames)
    elif type == "sign_verify":
        sign_verify_graph(filenames)
    else:
        logger.error("openssl_graph.py crypto|keyex|sign_verify FILE_NAME1 FILE_NAME2...")
        exit(1)


if __name__ == "__main__":
    main()
