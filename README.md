# jacoco-diff
在 jacoco 覆盖率报告的基础上，计算出增量覆盖率


# 结果展示
### 命令行提示
![图片](http://ovh9b5ele.bkt.clouddn.com/PNovOQMLbnfXfzbJbInE.png)

### 覆盖率报告

新增的行首增加蓝色钻石标志，与其它钻石不冲突

![图片](http://ovh9b5ele.bkt.clouddn.com/yAEHZSeukx8mwlH4lCNl.png)

# 用法
`
python main.py -d ~/jenkins_workspace/workspace/account_server -m account-impl -o HEAD~5
`

## 参数说明
  -h, --help                show this help message and exit
  
  -dir DIR                  工程根目录
  
  -old_version OLD_VERSION  指定对比的版本号, 如果该参数没有给出，默认与前一个版本进行对比(HEAD~1)。
                            该参数支持 git commit hash 或者 HEAD~n 的格式。
  -module MODULE            需要处理的子模块(如果制定的工程没有子模块，需要自行修改一些代码)
