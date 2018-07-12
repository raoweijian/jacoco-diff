#!/usr/bin/env python3
#coding=utf8

import os
import json
import sys
import re
import pprint
import shutil
import getopt
import argparse

from git import Repo

from diff_processor import DiffProcessor


def main(argv):
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="计算增量覆盖率的工具")
    parser.add_argument('-dir', type=str, help="工程根目录")
    parser.add_argument('-old_version', type=str, default="HEAD~1", help='指定对比的版本号')
    parser.add_argument('-module', type=str, help="需要处理的子模块")
    opts = parser.parse_args(argv[1:])
    if opts.dir is None or opts.module is None:
        parser.print_help()
        sys.exit()

    # 获取增量覆盖率信息
    processor = DiffProcessor(opts.dir, opts.old_version, opts.module)
    diff_cov_info = processor.process_diff()

    # 写入redis
    job_name = argv[4]
    build_id = argv[5]
    key = "{}-{}".format(job_name, build_id)

    # 拷贝 css 和图片资源
    shutil.copy('diff.gif', os.path.join(opts.dir, opts.module, "target/site/jacoco/jacoco-resources"))
    shutil.copy('report.css', os.path.join(opts.dir, opts.module, "target/site/jacoco/jacoco-resources"))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
