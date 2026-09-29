import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("smoke_probe.py")
SPEC = importlib.util.spec_from_file_location("smoke_probe", MODULE_PATH)
assert SPEC and SPEC.loader
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_sha256_text_is_stable():
    assert PROBE.sha256_text("synthetic") == (
        "b3cc0475bb78a5026098858e9889acf666d31062d513d303314eca31d36e72f2"
    )


def test_normalize_observation_hashes_canvas_and_sorts_extensions():
    result = PROBE.normalize_observation(
        {"canvasDataUrl": "data:image/png;base64,synthetic", "webglExtensions": ["Z", "A"]}
    )
    assert "canvasDataUrl" not in result
    assert result["canvasSha256"] == PROBE.sha256_text("data:image/png;base64,synthetic")
    assert result["webglExtensions"] == ["A", "Z"]


def test_normalize_observation_does_not_mutate_input():
    raw = {"canvasDataUrl": "x", "webglExtensions": ["B", "A"]}
    PROBE.normalize_observation(raw)
    assert raw == {"canvasDataUrl": "x", "webglExtensions": ["B", "A"]}
