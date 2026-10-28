# -*- coding: utf-8 -*-
"""把 sRGB 打印稿按 Epson 自带的纸张 ICC 转成打印机色彩空间(2026-10-27):
用法:python icc_convert.py <稿件.jpg> [velvet|matte] [perceptual|relative]
输出同目录 <稿件>_ICC-<纸>-<意图>.jpg,**不嵌色彩描述文件**(device RGB),配合 art_print_v2 的
  --opt EPIJ_CMat=3 --opt EPIJ_HdofClSp=0   (驱动不再校色、不把无描述文件的数据当 Generic RGB)
发送,相当于 Photoshop「由应用程序管理颜色 + 驱动 No Color Adjustment」。
为什么:10/27 用驱动「EPSON 标准」校色印海上渔夫 B 档,整体偏红;用 Epson 的 Velvet 配置文件软打样,暗部 a* 由 -1.4
变 +1.2、b* +1.6,说明这张纸+这台机的默认暗部本来就偏暖红,要靠 ICC 反向补偿。黑场补偿开,让画里最深处落到纸的最深黑。
"""
import pathlib, sys
from PIL import Image, ImageCms

ICC = {
    "velvet": "/Library/Printers/EPSON/InkjetPrinter2/ICCProfiles/EP2006NK2.profiles/Contents/Resources/EW-M873T Velvet Fine Art Paper.icc",
    "matte": "/Library/Printers/EPSON/InkjetPrinter2/ICCProfiles/EP2006NK2.profiles/Contents/Resources/EW-M873T Matte Paper.icc",
    "plain": "/Library/Printers/EPSON/InkjetPrinter2/ICCProfiles/EP2006NK2.profiles/Contents/Resources/EW-M873T Standard.icc",
}
INTENT = {"perceptual": ImageCms.Intent.PERCEPTUAL, "relative": ImageCms.Intent.RELATIVE_COLORIMETRIC}

src = pathlib.Path(sys.argv[1]); paper = sys.argv[2] if len(sys.argv) > 2 else "velvet"; intent = sys.argv[3] if len(sys.argv) > 3 else "perceptual"
im = Image.open(src)
info = im.info
srgb = ImageCms.createProfile("sRGB")
inp = ImageCms.ImageCmsProfile(__import__("io").BytesIO(info["icc_profile"])) if info.get("icc_profile") else srgb
tf = ImageCms.buildTransform(inp, ImageCms.getOpenProfile(ICC[paper]), "RGB", "RGB", renderingIntent=INTENT[intent],
                             flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
out = ImageCms.applyTransform(im.convert("RGB"), tf)
dst = src.with_name(f"{src.stem}_ICC-{paper}-{intent}.jpg")
out.save(dst, quality=95, subsampling=0, dpi=info.get("dpi", (360, 360)))   # 不嵌 icc_profile
print("wrote", dst)
