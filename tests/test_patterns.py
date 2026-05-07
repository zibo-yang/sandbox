"""Tests for injection_detector.patterns."""

import re

import pytest

from injection_detector.patterns import PATTERNS

VALID_SEVERITIES = {"low", "medium", "high"}
REQUIRED_KEYS = {"name", "pattern", "severity", "description"}


class TestPatternsCollection:
    """Tests for the top-level PATTERNS list."""

    def test_patterns_is_a_list(self):
        assert isinstance(PATTERNS, list)

    def test_patterns_is_not_empty(self):
        assert len(PATTERNS) > 0, "PATTERNS must contain at least one entry"


class TestPatternEntryStructure:
    """Tests that every entry in PATTERNS has the required shape."""

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_has_required_keys(self, entry):
        missing = REQUIRED_KEYS - entry.keys()
        assert not missing, f"Pattern entry is missing keys: {missing}"

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_name_is_non_empty_string(self, entry):
        assert isinstance(entry["name"], str)
        assert entry["name"].strip(), "Pattern 'name' must not be blank"

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_description_is_non_empty_string(self, entry):
        assert isinstance(entry["description"], str)
        assert entry["description"].strip(), "Pattern 'description' must not be blank"

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_pattern_field_is_string(self, entry):
        assert isinstance(entry["pattern"], str), "'pattern' field must be a string"

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_pattern_regex_compiles(self, entry):
        try:
            re.compile(entry["pattern"], re.IGNORECASE)
        except re.error as exc:
            pytest.fail(
                f"Pattern '{entry['name']}' has an invalid regex: {exc}"
            )

    @pytest.mark.parametrize("entry", PATTERNS, ids=lambda e: e.get("name", "<unnamed>"))
    def test_severity_is_valid(self, entry):
        assert entry["severity"] in VALID_SEVERITIES, (
            f"Pattern '{entry['name']}' has invalid severity '{entry['severity']}'. "
            f"Must be one of {VALID_SEVERITIES}."
        )
