"""Windows DPAPI and Job Object feasibility probes for AUD-031/AUD-034.

Research code only. The production adapter remains a Rust Phase 2 task after
the applicable audit and architecture gates are accepted.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import subprocess
import sys
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CRYPTPROTECT_UI_FORBIDDEN = 0x1
CREATE_SUSPENDED = 0x00000004
CREATE_NO_WINDOW = 0x08000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
WAIT_OBJECT_0 = 0
STILL_ACTIVE = 259


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


class STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in (
        "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
        "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
    )]


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


def _require_windows() -> None:
    if os.name != "nt":
        raise RuntimeError("WINDOWS_REQUIRED")


def _blob(data: bytes) -> tuple[DATA_BLOB, Any]:
    buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    return DATA_BLOB(len(data), buffer), buffer


def dpapi_protect(data: bytes, entropy: bytes) -> bytes:
    _require_windows()
    in_blob, in_buffer = _blob(data)
    entropy_blob, entropy_buffer = _blob(entropy)
    out_blob = DATA_BLOB()
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    ok = crypt32.CryptProtectData(
        ctypes.byref(in_blob), None, ctypes.byref(entropy_blob), None, None,
        CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out_blob),
    )
    _ = (in_buffer, entropy_buffer)
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel32.LocalFree(out_blob.pbData)


def dpapi_unprotect(ciphertext: bytes, entropy: bytes) -> bytes:
    _require_windows()
    in_blob, in_buffer = _blob(ciphertext)
    entropy_blob, entropy_buffer = _blob(entropy)
    out_blob = DATA_BLOB()
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    ok = crypt32.CryptUnprotectData(
        ctypes.byref(in_blob), None, ctypes.byref(entropy_blob), None, None,
        CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out_blob),
    )
    _ = (in_buffer, entropy_buffer)
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel32.LocalFree(out_blob.pbData)


def probe_dpapi() -> dict[str, Any]:
    plaintext = b"synthetic-secret-not-a-credential"
    entropy = b"multi-profiles/aud-034/v1"
    ciphertext = dpapi_protect(plaintext, entropy)
    wrong_entropy_rejected = False
    try:
        dpapi_unprotect(ciphertext, b"wrong-purpose")
    except OSError:
        wrong_entropy_rejected = True
    return {
        "roundTrip": dpapi_unprotect(ciphertext, entropy) == plaintext,
        "ciphertextDiffers": ciphertext != plaintext,
        "wrongEntropyRejected": wrong_entropy_rejected,
        "ciphertextLength": len(ciphertext),
        "plaintextPersisted": False,
    }


def _check(ok: Any) -> None:
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())


def probe_job_object() -> dict[str, Any]:
    _require_windows()
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.CreateProcessW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
        wintypes.BOOL, wintypes.DWORD, ctypes.c_void_p, wintypes.LPCWSTR,
        ctypes.POINTER(STARTUPINFOW), ctypes.POINTER(PROCESS_INFORMATION),
    ]
    job = kernel32.CreateJobObjectW(None, None)
    _check(job)
    process_info = PROCESS_INFORMATION()
    try:
        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        _check(kernel32.SetInformationJobObject(
            job,
            JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ))
        command = subprocess.list2cmdline([sys.executable, "-c", "import time; time.sleep(60)"])
        mutable_command = ctypes.create_unicode_buffer(command)
        startup = STARTUPINFOW()
        startup.cb = ctypes.sizeof(startup)
        _check(kernel32.CreateProcessW(
            sys.executable,
            mutable_command,
            None,
            None,
            False,
            CREATE_SUSPENDED | CREATE_NO_WINDOW | CREATE_UNICODE_ENVIRONMENT,
            None,
            None,
            ctypes.byref(startup),
            ctypes.byref(process_info),
        ))
        _check(kernel32.AssignProcessToJobObject(job, process_info.hProcess))
        if kernel32.ResumeThread(process_info.hThread) == 0xFFFFFFFF:
            raise ctypes.WinError(ctypes.get_last_error())
        kernel32.CloseHandle(process_info.hThread)
        process_info.hThread = None
        alive_before_close = kernel32.WaitForSingleObject(process_info.hProcess, 0) != WAIT_OBJECT_0
        _check(kernel32.CloseHandle(job))
        job = None
        terminated = kernel32.WaitForSingleObject(process_info.hProcess, 5000) == WAIT_OBJECT_0
        exit_code = wintypes.DWORD()
        _check(kernel32.GetExitCodeProcess(process_info.hProcess, ctypes.byref(exit_code)))
        return {
            "createdSuspended": True,
            "assignedBeforeResume": True,
            "aliveBeforeJobClose": alive_before_close,
            "terminatedOnJobClose": terminated,
            "exitCodeWasActiveAfterWait": exit_code.value == STILL_ACTIVE,
        }
    finally:
        if process_info.hThread:
            kernel32.CloseHandle(process_info.hThread)
        if process_info.hProcess:
            kernel32.CloseHandle(process_info.hProcess)
        if job:
            kernel32.CloseHandle(job)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schemaVersion": "0.1.0",
        "kind": "windows-security-primitives",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "dpapiCurrentUser": probe_dpapi(),
        "jobObject": probe_job_object(),
        "limits": [
            "No different-user DPAPI test was performed",
            "No Camoufox tree was placed in the test Job Object",
            "Same-user malware remains outside the protection claim",
        ],
    }
    dpapi = result["dpapiCurrentUser"]
    job = result["jobObject"]
    result["passed"] = (
        dpapi["roundTrip"]
        and dpapi["ciphertextDiffers"]
        and dpapi["wrongEntropyRejected"]
        and not dpapi["plaintextPersisted"]
        and job["createdSuspended"]
        and job["assignedBeforeResume"]
        and job["aliveBeforeJobClose"]
        and job["terminatedOnJobClose"]
        and not job["exitCodeWasActiveAfterWait"]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
