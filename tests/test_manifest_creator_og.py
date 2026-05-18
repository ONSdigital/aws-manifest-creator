import os
import pytest

from argparse import Namespace
from manifest_creator_og import validate

@pytest.fixture
def allargs():
    return Namespace(
        path=os.getcwd(),
        sourceName="ons_tdz",
        description="Test dataset for validation",
        version="1",
        dataset="valid_dataset",
        sensitivity="low",
        iterationl1=None,
        iterationl2=None,
        iterationl3=None,
        iterationl4=None
    )

def test_validate_returns_true(allargs):
    # act
    result = validate(allargs)

    # assert
    assert result == True


def test_validate_rejects_invalid_path(allargs):
    # arrange
    allargs.path = "None"   # invalid path

    # act
    result = validate(allargs)

    # assert
    assert result == False


def test_validate_rejects_invalid_characters(allargs):
    # arrange
    allargs.dataset = "INVALID dataset name"

    # act
    result = validate(allargs)

    # assert
    assert result == False


@pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
def test_validate_rejects_invalid_characters_in_iteration1(allargs):
    # arrange
    allargs.iterationl1 = "INVALID iteration!!!"

    # act
    result = validate(allargs)

    # assert
    assert result == False


@pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
def test_validate_rejects_invalid_characters_in_iteration2(allargs):
    # arrange
    allargs.iterationl2 = "INVALID iteration!!!"

    # act
    result = validate(allargs)

    # assert
    assert result == False


@pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
def test_validate_rejects_invalid_characters_in_iteration3(allargs):
    # arrange
    allargs.iterationl3 = "INVALID iteration!!!"

    # act
    result = validate(allargs)

    # assert
    assert result == False


@pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
def test_validate_rejects_invalid_characters_in_iteration4(allargs):
    # arrange
    allargs.iterationl4 = "INVALID iteration!!!"

    # act
    result = validate(allargs)

    # assert
    assert result == False


def test_validate_rejects_invalid_version(allargs):
    # arrange
    allargs.version = 100

    # act
    result = validate(allargs)

    # assert
    assert result == False


def test_validate_rejects_invalid_sensitivity_level(allargs):
    # arrange
    allargs.sensitivity = "INVALID sensitivity level!!!"

    # act
    result = validate(allargs)

    # assert
    assert result == False