# ttf-to-woff2

该脚本用于将 TTF 字体精简压缩为 Woff2 字体。

用法：

```powershell
PS C:\Users\ykla> pip install fonttools brotli 
PS C:\Users\ykla> python C:\Users\ykla\Desktop\woff2.py  D:\LXGWWenKaiMonoGBScreen.ttf  changgui22m.woff2 C:\Users\ykla\Desktop\zi.txt
```

- `D:\LXGWWenKaiMonoGBScreen.ttf` 是原字体名。
- `changgui22m.woff2` 是要生成的 woff2 字体名。
- `C:\Users\ykla\Desktop\zi.txt` 是汉字表，每行一个字，换行符为 UNIX 换行符，编码 UTF-8
