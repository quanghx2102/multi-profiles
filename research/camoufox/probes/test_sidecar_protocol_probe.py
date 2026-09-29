import importlib.util
import json
import struct
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("sidecar_protocol_probe.py")
SPEC = importlib.util.spec_from_file_location("sidecar_protocol_probe", MODULE_PATH)
assert SPEC and SPEC.loader
PROTOCOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROTOCOL)


def test_frame_round_trip_is_canonical():
    message = {"protocolVersion": "1.0.0", "requestId": "synthetic", "payload": {"b": 2, "a": 1}}
    frame = PROTOCOL.encode_frame(message)
    assert PROTOCOL.decode_frame(frame) == message
    assert frame[4:] == json.dumps(message, separators=(",", ":"), sort_keys=True).encode()


@pytest.mark.parametrize(
    "frame,error",
    [
        (b"", "FRAME_HEADER_TRUNCATED"),
        (struct.pack(">I", 0), "FRAME_SIZE_INVALID"),
        (struct.pack(">I", 2) + b"{}x", "FRAME_LENGTH_MISMATCH"),
        (struct.pack(">I", 1) + b"[", "FRAME_JSON_INVALID"),
        (struct.pack(">I", 2) + b"[]", "FRAME_ROOT_INVALID"),
    ],
)
def test_invalid_frames_fail_closed(frame, error):
    with pytest.raises(PROTOCOL.ProtocolViolation, match=error):
        PROTOCOL.decode_frame(frame)


def test_oversized_frame_is_rejected_before_transport():
    with pytest.raises(PROTOCOL.ProtocolViolation, match="FRAME_SIZE_INVALID"):
        PROTOCOL.encode_frame({"value": "x" * PROTOCOL.MAX_FRAME_BYTES})


def test_challenge_proof_binds_session_profile_and_instance():
    token = b"t" * PROTOCOL.SESSION_TOKEN_BYTES
    nonce = b"n" * PROTOCOL.NONCE_BYTES
    proof = PROTOCOL.challenge_proof(token, nonce, "sidecar-1", "profile-1")
    assert PROTOCOL.verify_challenge_proof(token, nonce, "sidecar-1", "profile-1", proof)
    assert not PROTOCOL.verify_challenge_proof(token, nonce, "sidecar-2", "profile-1", proof)
    assert not PROTOCOL.verify_challenge_proof(token, nonce, "sidecar-1", "profile-2", proof)
    assert not PROTOCOL.verify_challenge_proof(b"x" * 32, nonce, "sidecar-1", "profile-1", proof)


def test_auth_material_size_is_exact():
    with pytest.raises(PROTOCOL.ProtocolViolation, match="AUTH_MATERIAL_SIZE_INVALID"):
        PROTOCOL.challenge_proof(b"short", b"n" * 32, "sidecar", "profile")
