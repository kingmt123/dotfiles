# Hindsight Memory Backup

Hindsight 记忆系统备份方案。自动导出所有记忆、配置、mental models 到 JSON。

## 目录结构

```
hindsight-backup/
├── README.md          # 本文件
├── backup.sh          # 备份脚本（可 cron 定时执行）
├── export/            # 导出数据（每次备份生成一个带时间戳的子目录）
│   └── 2026-05-25_180222/
│       ├── bank-export.json       # 银行配置 + mental models
│       ├── bank-config.json       # 银行详细配置
│       ├── bank-profile.json      # 银行 profile（disposition, mission）
│       ├── bank-stats.json        # 统计数据（节点数、链接数、观察数）
│       ├── memories.json          # 所有记忆（observations + facts）
│       └── tags.json              # 标签统计
```

## 使用

```bash
# 手动执行备份
./backup.sh

# 或通过 python 直接执行
python hindsight-backup.py
```

## 恢复

详见 `restore.md`。
