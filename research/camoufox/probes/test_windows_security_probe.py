import importlib.util
import os
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows-only primitives")
MODULE_PATH = Path(__file__).with_name("windows_security_probe.py")
SPEC = importlib.util.spec_from_file_location("windows_security_probe", MODULE_PATH)
assert SPEC and SPEC.loader
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_dpapi_current_user_round_trip_and_purpose_binding():
    result = PROBE.probe_dpapi()
    assert result["roundTrip"]
    assert result["ciphertextDiffers"]
    assert result["wrongEntropyRejected"]
    assert not result["plaintextPersisted"]


def test_job_object_kills_suspended_assigned_process_on_close():
    result = PROBE.probe_job_object()
    assert result["createdSuspended"]
    assert result["assignedBeforeResume"]
    assert result["aliveBeforeJobClose"]
    assert result["terminatedOnJobClose"]
    assert not result["exitCodeWasActiveAfterWait"]
