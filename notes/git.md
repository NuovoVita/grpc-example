** 常用 Git 场景命令

```bash
# 将 master 分支名称修改未 main 分支
git branch -m master main

# 本地分支添加远程分支，起名叫 origin
git remote add origin https://github.com/NuovoVita/grpc-example.git

# 本地分支关联远程分支，远程 origin 下面的 main 分支关联本地 main 分支
git branch --set-upstream-to=origin/main main
```
