#!/bin/bash
# 发布小红书笔记

# 读取最新内容
CONTENT_FILE="/root/.openclaw/workspace/memory/xiaohongshu_posts.md"

echo "读取内容..."
if [ ! -f "$CONTENT_FILE" ]; then
    echo "错误：找不到内容文件"
    exit 1
fi

echo "========================================="
echo "小红书发布脚本"
echo "========================================="
echo ""
echo "请复制以下内容到小红书发布："
echo ""
head -50 "$CONTENT_FILE"
echo ""
echo "========================================="
echo "完整内容已保存在: $CONTENT_FILE"
echo "========================================="
