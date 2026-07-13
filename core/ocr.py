"""OCR 模块：使用 PaddleOCR 2.x 从图片提取文字。

懒加载 PaddleOCR 实例（首次调用时初始化，避免启动卡顿）。

PaddleOCR 2.x API：
- 创建实例：PaddleOCR(use_angle_cls=True, lang='ch')
- 调用：ocr.ocr(image_path, cls=True) 返回 [[(box, (text, score)), ...]]
- 必须设置 FLAGS_use_mkldnn=0 避免 paddlepaddle 2.6 兼容性问题
"""

import os

# 必须在导入 paddle 前设置，禁用 oneDNN
os.environ.setdefault('FLAGS_use_mkldnn', '0')

_ocr_instance = None


def _get_ocr():
    global _ocr_instance
    if _ocr_instance is None:
        from paddleocr import PaddleOCR
        # PaddleOCR 2.x：lang='ch' 中文，use_angle_cls=True 启用方向分类
        _ocr_instance = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    return _ocr_instance


def _parse_result(result) -> str:
    """从 PaddleOCR 2.x 的 ocr() 结果中提取文本。

    result 结构: [page_result] → page_result = [(box, (text, score)), ...]
    """
    lines = []
    if not result:
        return ""
    # 2.x 返回 [[(box, (text, score)), ...]]；第一层是页列表
    for page in result:
        if not page:
            continue
        for item in page:
            # item = (box, (text, score))
            if not item or len(item) < 2:
                continue
            text_info = item[1]
            if not text_info or len(text_info) < 1:
                continue
            text = text_info[0]
            if text and str(text).strip():
                lines.append(str(text).strip())
    return "\n".join(lines)


def extract_text_from_image(image_path: str) -> str:
    """从图片提取文字，返回拼接后的纯文本。

    Args:
        image_path: 图片文件路径

    Returns:
        提取的文字内容，按行拼接
    """
    # 不吞异常：让错误冒泡到 API 层，前端能看到具体原因
    ocr = _get_ocr()
    result = ocr.ocr(image_path, cls=True)
    return _parse_result(result)


def extract_text_from_bytes(image_bytes: bytes) -> str:
    """从图片字节流提取文字。

    Args:
        image_bytes: 图片二进制数据

    Returns:
        提取的文字内容
    """
    import tempfile
    import os
    # 写入临时文件（PaddleOCR 需要文件路径）
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        f.write(image_bytes)
        tmp_path = f.name
    try:
        return extract_text_from_image(tmp_path)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

