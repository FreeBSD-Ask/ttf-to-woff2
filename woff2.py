import sys
import os
from fontTools import subset

def read_chars_from_file(file_path):
    """从文本文件读取汉字并返回Unicode范围字符串"""
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            chars = set()
            for line in f:
                line = line.strip()
                if line:
                    # 将每行的每个字符单独处理
                    for char in line:
                        if ord(char) > 127:  # 主要处理非ASCII字符（汉字等）
                            chars.add(char)
            
            if not chars:
                print(f"警告: 文件 '{file_path}' 中没有找到有效的汉字字符")
                return ""
            
            # 将字符转换为U+XXXX格式
            unicode_list = [f"U+{ord(char):04X}" for char in chars]
            unicode_ranges = ",".join(unicode_list)
            print(f"从文件读取了 {len(chars)} 个唯一字符")
            return unicode_ranges
            
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)

def subset_font(input_path, output_path, char_file=None):
    options = subset.Options()
    options.flavor = "woff2"
    options.drop_tables += ['FFTM', 'DSIG', 'GPOS', 'GSUB', 'name']
    options.no_hinting = True

    # 基础Unicode范围（拉丁字母、标点符号等）
    base_unicode_ranges = (
        "U+0020-007E,"  # 基本拉丁字母
        "U+00A0-00FF,U+0100-017F,U+0180-024F,"  # 扩展拉丁字母
        "U+2000-206F,U+3000-303F,"  # 标点符号
        "U+3040-309F,U+30A0-30FF,"  # 日文假名
        "U+FF00-FFEF"  # 全角字符
    )

    # 如果提供了字符文件，从中读取汉字
    char_unicode_ranges = ""
    if char_file:
        char_unicode_ranges = read_chars_from_file(char_file)
    
    # 合并所有Unicode范围
    if char_unicode_ranges:
        unicode_ranges = base_unicode_ranges + "," + char_unicode_ranges
    else:
        unicode_ranges = base_unicode_ranges

    print(f"使用的Unicode范围: {unicode_ranges[:100]}...")  # 只打印前100字符避免过长

    try:
        subsetter = subset.Subsetter(options)
        subsetter.populate(unicodes=subset.parse_unicodes(unicode_ranges))

        font = subset.load_font(input_path, options)
        subsetter.subset(font)
        subset.save_font(font, output_path, options)
        print(f"字体子集化完成: {output_path}")
        
    except Exception as e:
        print(f"字体处理出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python subset_font.py 输入字体.ttf 输出字体.woff2 [字符文件.txt]")
        print("示例: python subset_font.py font.ttf font.woff2")
        print("示例: python subset_font.py font.ttf font.woff2 characters.txt")
        sys.exit(1)
    
    input_font = sys.argv[1]
    output_font = sys.argv[2]
    char_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    subset_font(input_font, output_font, char_file)
