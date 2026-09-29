"""Research-only framing and session-authentication primitives for AUD-024.

This module does not select or implement the Windows transport. It exercises
the byte-level rules that a named-pipe implementation must enforce.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import struct
from typing import Any


PROTOCOL_VERSION = "1.0.0-draft"
MAX_FRAME_BYTES = 1024 * 1024
NONCE_BYTES = 32
SESSION_TOKEN_BYTES = 32


class ProtocolViolation(ValueError):
    pass


def encode_frame(message: dict[str, Any]) -> bytes:
    body = json.dumps(message, separators=(",", ":"), sort_keys=True).encode("utf-8")
    if not body or len(body) > MAX_FRAME_BYTES:
        raise ProtocolViolation("FRAME_SIZE_INVALID")
    return struct.pack(">I", len(body)) + body


def decode_frame(frame: bytes) -> dict[str, Any]:
    if len(frame) < 4:
        raise ProtocolViolation("FRAME_HEADER_TRUNCATED")
    declared = struct.unpack(">I", frame[:4])[0]
    if declared == 0 or declared > MAX_FRAME_BYTES:
        raise ProtocolViolation("FRAME_SIZE_INVALID")
    body = frame[4:]
    if len(body) != declared:
        raise ProtocolViolation("FRAME_LENGTH_MISMATCH")
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolViolation("FRAME_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise ProtocolViolation("FRAME_ROOT_INVALID")
    return value


def new_session_token() -> bytes:
    return secrets.token_bytes(SESSION_TOKEN_BYTES)


def new_challenge() -> bytes:
    return secrets.token_bytes(NONCE_BYTES)


def challenge_proof(
    token: bytes, nonce: bytes, sidecar_instance_id: str, profile_id: str
) -> str:
    if len(token) != SESSION_TOKEN_BYTES or len(nonce) != NONCE_BYTES:
        raise ProtocolViolation("AUTH_MATERIAL_SIZE_INVALID")
    transcript = b"\x00".join(
        (
            PROTOCOL_VERSION.encode("ascii"),
            nonce,
            sidecar_instance_id.encode("utf-8"),
            profile_id.encode("utf-8"),
        )
    )
    return hmac.new(token, transcript, hashlib.sha256).hexdigest()


def verify_challenge_proof(
    token: bytes,
    nonce: bytes,
    sidecar_instance_id: str,
    profile_id: str,
    proof: str,
) -> bool:
    expected = challenge_proof(token, nonce, sidecar_instance_id, profile_id)
    return hmac.compare_digest(expected, proof)
