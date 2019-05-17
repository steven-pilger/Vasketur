import pytest

from vasketur.machinestate.utilities import (
    extract_cookie,
    extract_machine_state,
    parse_machine_state,
    convert_scandi_chars,
)

from requests_html import Element


def test_request_cookie(fixture_cookie_request):
    assert fixture_cookie_request.status_code == 200


def test_extract_cookie(fixture_cookie_request):
    c = extract_cookie(fixture_cookie_request)
    assert type(c) is str


def test_request_machine_state(fixture_machine_state):
    rms = fixture_machine_state
    page_content = rms.html.text
    assert "Glemt kode" not in page_content


def test_extract_machine_state(fixture_machine_state):
    rms = fixture_machine_state
    ms = extract_machine_state(rms)
    assert type(ms[0]) is Element


def test_convert_scandi_chars():
    test_char = "Ã¸"
    comp_char = "ø"
    assert convert_scandi_chars(test_char) == comp_char


def test_parse_machine_state(fixture_machine_state):
    rms = fixture_machine_state
    ms = extract_machine_state(rms)
    ms = parse_machine_state(ms)
    assert "wash" in ms[0]["machine_type"].lower()
