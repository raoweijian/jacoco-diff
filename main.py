#!/usr/bin/env python3
# coding=utf8

import os
import sys
import shutil
import argparse

from diff_processor import DiffProcessor


def main(argv):
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="计算增量覆盖率的工具")
    parser.add_argument('-dir', type=str, help="工程根目录")
    parser.add_argument('-old_version', type=str, default="HEAD~1", help='指定对比的版本号')
    opts = parser.parse_args(argv[1:])
    if opts.dir is None:
        parser.print_help()
        sys.exit()

    # 获取增量覆盖率信息
    processor = DiffProcessor(opts.dir, opts.old_version)
    diff_cov_info = processor.process_diff()

    # 拷贝 css 和图片资源
    shutil.copy('diff.gif', os.path.join(opts.dir, "target/site/jacoco/jacoco-resources"))
    shutil.copy('report.css', os.path.join(opts.dir, "target/site/jacoco/jacoco-resources"))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
