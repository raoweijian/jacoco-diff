import re
import os

from git import Repo


class DiffProcessor():
    def __init__(self, project_dir, old_version):
        self.project_dir = project_dir
        self.old_version = old_version
        self.repo = Repo(self.project_dir)

    def resolve_file_info(self, file_name):
        full_path = os.path.join(self.project_dir, file_name)
        package = self.get_package(full_path)

        class_ = re.search('(\w+)\.java$', file_name).group(1)

        is_interface = self.is_interface(full_path)

        return (package, class_, is_interface)

    def get_package(self, file_name):
        """获取package名"""
        ret = ''
        with open(file_name) as fp:
            for line in fp:
                line = line.strip()
                match = re.match('package\s+(\S+);', line)
                if match:
                    ret = match.group(1)
                    break
        return ret

    def is_interface(self, file_name):
        """判断某个文件是否是接口"""
        ret = False
        name = re.search('(\w+)\.java$', file_name).group(1)
        reg_interface = re.compile('public\s+interface\s+{}'.format(name))
        with open(file_name) as fp:
            for line in fp:
                line = line.strip()
                match = re.match(reg_interface, line)
                if match:
                    ret = True
                    break
        return ret

    def get_diff(self):
        """获取diff详情"""
        diff = self.repo.git.diff(self.old_version, self.repo.head).split("\n")
        ret = {}

        file_name = ""
        diff_lines = []
        current_line = 0
        for line in diff:
            if line.startswith('diff --git'):
                # 进入新的block
                if file_name != "":
                    ret[file_name] = diff_lines
                file_name = re.findall('b/(\S+)$', line)[0]
                diff_lines = []
                current_line = 0

            elif re.match('@@ -\d+,\d+ \+(\d+),\d+ @@', line):
                match = re.match('@@ -\d+,\d+ \+(\d+),\d+ @@', line)
                current_line = int(match.group(1)) - 1

            elif line.startswith("-"):
                continue
            elif line.startswith("+") and not line.startswith('+++'):
                current_line += 1
                diff_lines.append(current_line)
            else:
                current_line += 1
        ret[file_name] = diff_lines

        return ret

    def modify_html(self, html_file_name, diff_lines):
        new_line_count = 0
        cover_line_count = 0

        content = []
        with open(html_file_name, 'r') as fp:
            content = fp.readlines()

        for i in range(1, len(content)):
            if i + 1 in diff_lines:
                match = re.search('class="([^"]+)"', content[i])
                if match:
                    content[i] = re.sub('class="([^"]+)"', lambda m: 'class="{}-diff"'.format(m.group(1)), content[i])
                    css_class = match.group(1)
                    new_line_count += 1
                    if css_class.startswith("fc") or css_class.startswith("pc"):
                        cover_line_count += 1

        with open(html_file_name, 'w') as fp:
            fp.write("".join(content))

        return new_line_count, cover_line_count

    def process_diff(self):
        ret = {}
        diff_result = self.get_diff()

        for file_name in diff_result:
            # 过滤掉只有删除，没有新增的代码
            if diff_result[file_name] == []:
                continue

            # 过滤掉非 java 文件和测试代码
            if not file_name.endswith(".java") or 'src/test/java/' in file_name:
                continue

            package, class_, is_interface = self.resolve_file_info(file_name)
            # 过滤掉接口和非指定的module
            if is_interface:
                continue

            html_file_name = os.path.join(self.project_dir, 'target/site/jacoco/', package, "{}.java.html".format(class_))
            new_line_count, cover_line_count = self.modify_html(html_file_name, diff_result[file_name])
            print("package {}, class {}, 新增 {} 行, 覆盖 {} 行".format(package, class_, new_line_count, cover_line_count))

            # 信息存进返回值
            if package not in ret:
                ret[package] = {}
            ret[package][class_] = {"new": new_line_count, "cover": cover_line_count}

        return ret
