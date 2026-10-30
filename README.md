Student @ Tsinghua (IIIS). 

Interest in trapped-ion quantum computing, quantum information & AI4Science. 

## 开源项目与在线文档

[访问开源仓库手册](https://xiaoshecode.github.io/xiaoshecode/) · [本仓库维护文档](https://xiaoshecode.github.io/xiaoshecode/repos/xiaoshecode/)

手册为 30 个公开仓库分别整理用途、环境准备、使用入口、目录结构、检查结果和已知限制，并区分原创项目与 Fork。各项目 README 提供对应页面入口。

## 文档维护

本仓库同时提供 GitHub 个人资料 README 和公开项目手册。资料快照日期：2026-10-30。

```sh
python scripts/build_docs.py
python scripts/check_docs.py
python -m http.server 8000 --directory docs
```

需要 Python 3.10+，构建脚本仅使用标准库。预览地址为 `http://localhost:8000/`。

| 目录 | 职责 |
| --- | --- |
| `data/repositories/` | 每个项目的结构化文档与验证记录 |
| `scripts/build_docs.py` | 生成索引及项目页面 |
| `scripts/check_docs.py` | 检查记录完整性和站内链接 |
| `docs/assets/` | 页面样式与浏览器端搜索 |
| `docs/repos/` | 生成的独立项目文档 |
| `docs/index.html` | 文档中心入口 |

修改资料后重新生成并检查页面，将源数据和生成结果一并提交。GitHub Pages 从 `main` 分支的 `/docs` 发布，不需要额外框架或构建服务。验证记录须写明命令、环境与局限，不能将静态检查表述为实机测试。

