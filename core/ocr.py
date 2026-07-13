"""OCR 模块：使用 RapidOCR (ONNX Runtime) 从图片提取文字。

RapidOCR 使用 PaddleOCR 同款模型但走 ONNX Runtime 推理，不依赖
paddlepaddle，无需 AVX 指令集，内存占用约 300MB，适合轻量服务器。

API：
- 创建实例：RapidOCR()
- 调用：result, elapse = ocr(img_path) → result = [[box, text, score], ...]
"""

_ocr_instance = None


def _get_ocr():
    global _ocr_instance
    if _ocr_instance is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_instance = RapidOCR()
    return _ocr_instance


def _parse_result(result) -> str:
    """从 RapidOCR 结果中提取文本。

    result 结构: [[box, text, score], [box, text, score], ...] 或 None
    """
    if not result:
        return ""
    lines = []
    for item in result:
        # item = [box, text, score]
        if not item or len(item) < 2:
            continue
        text = item[1]
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
    ocr = _get_ocr()
    result, elapse = ocr(image_path)
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
