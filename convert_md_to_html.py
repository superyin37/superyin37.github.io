#!/usr/bin/env python3
"""
Markdown to HTML Converter
批量将项目文件夹中的Markdown文件转换为HTML
"""

import os
import re
from pathlib import Path

def read_md_file(md_path):
    """读取Markdown文件"""
    with open(md_path, 'r', encoding='utf-8') as f:
        return f.read()

def simple_md_to_html(md_content):
    """简单的Markdown到HTML转换"""
    html = md_content
    
    # 代码块
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # 粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 图片
    html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<figure><img src="\2" alt="\1" /><figcaption>\1</figcaption></figure>', html)
    
    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 列表
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html, flags=re.MULTILINE)
    
    # 水平线
    html = re.sub(r'^---+$', r'<hr />', html, flags=re.MULTILINE)
    
    # 段落
    lines = html.split('\n')
    in_list = False
    in_pre = False
    result = []
    
    for line in lines:
        if '<pre>' in line:
            in_pre = True
        if '</pre>' in line:
            in_pre = False
            
        if line.strip().startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(line)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            
            if line.strip() and not line.startswith('<') and not in_pre:
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def create_html_template(title, content, lang='en'):
    """创建HTML模板"""
    template = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../../style.css" />
  <style>
    body {{ font-family: 'Inter', 'Noto Sans JP', sans-serif; line-height: 1.7; background: #fafafa; color: #222; }}
    .project-page {{ max-width: 900px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    .back-link {{ display: inline-block; margin-bottom: 1rem; text-decoration: none; color: #005bbb; font-weight: 600; }}
    h1, h2, h3, h4 {{ color: #111; margin-top: 1.5rem; }}
    hr {{ margin: 2rem 0; border: none; border-top: 1px solid #eee; }}
    ul {{ padding-left: 1.5rem; }}
    pre {{ background: #f4f4f4; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
    code {{ background: #f0f0f0; padding: 0.2rem 0.4rem; border-radius: 3px; font-family: 'Courier New', monospace; }}
    pre code {{ background: none; padding: 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
    table th, table td {{ border: 1px solid #ddd; padding: 0.75rem; text-align: left; }}
    figure {{ margin: 1.5rem 0; }}
    figure img {{ width: 100%; border-radius: 8px; }}
    figure figcaption {{ font-size: 0.9rem; color: #666; margin-top: 0.5rem; text-align: center; }}
    blockquote {{ border-left: 4px solid #005bbb; padding-left: 1rem; margin: 1rem 0; color: #555; }}
  </style>
</head>
<body>
  <main class="project-page">
    <a class="back-link" href="../../index.html">&larr; Back to Home</a>
    <article>
{content}
    </article>
  </main>
</body>
</html>"""
    return template

def convert_md_to_html(md_path, output_path):
    """转换单个Markdown文件到HTML"""
    print(f"转换: {md_path} -> {output_path}")
    
    # 读取Markdown
    md_content = read_md_file(md_path)
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Project Details"
    
    # 判断语言
    lang = 'ja' if ('_jp' in str(md_path) or '日本' in md_content[:500]) else 'en'
    
    # 转换内容
    html_content = simple_md_to_html(md_content)
    
    # 生成完整HTML
    full_html = create_html_template(title, html_content, lang)
    
    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ 完成: {output_path}")

def main():
    """主函数：批量转换"""
    base_dir = Path(__file__).parent / 'projects'
    
    # 定义要转换的文件
    files_to_convert = [
        ('ArchLink/archLink_en.md', 'ArchLink/archLink_en.html'),
        ('ArchLink/archLink_jp.md', 'ArchLink/archLink_jp.html'),
        ('Fraud/fraud_en.md', 'Fraud/fraud_en.html'),
        ('Fraud/fraud_jp.md', 'Fraud/fraud_jp.html'),
        ('Trash/trash_en.md', 'Trash/trash_en.html'),
        ('Trash/trash_jp.md', 'Trash/trash_jp.html'),
    ]
    
    print("=" * 60)
    print("开始批量转换 Markdown -> HTML")
    print("=" * 60)
    
    for md_file, html_file in files_to_convert:
        md_path = base_dir / md_file
        html_path = base_dir / html_file
        
        if md_path.exists():
            try:
                convert_md_to_html(md_path, html_path)
            except Exception as e:
                print(f"✗ 错误: {md_file} - {e}")
        else:
            print(f"⚠ 跳过: {md_file} (文件不存在)")
    
    print("=" * 60)
    print("转换完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
