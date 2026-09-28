import pytest
from app.services.weather_service import detect_location


def test_detects_managua():
    assert detect_location("vivo en Managua y mis plantas estan mal") == "Managua,NI"


def test_detects_matagalpa():
    assert detect_location("Estoy en Matagalpa, mis matas de cafe tienen hojas amarillas") == "Matagalpa,NI"


def test_detects_leon():
    assert detect_location("trabajo en Leon con maiz") == "Leon,NI"


def test_detects_esteli():
    assert detect_location("mis cultivos en Esteli necesitan ayuda") == "Esteli,NI"


def test_detects_granada():
    assert detect_location("soy de Granada") == "Granada,NI"


def test_detects_chinandega():
    assert detect_location("tengo una finca en Chinandega") == "Chinandega,NI"


def test_detects_rivas():
    assert detect_location("la siembra en Rivas esta afectada") == "Rivas,NI"


def test_returns_none_when_no_city_found():
    assert detect_location("mis plantas tienen manchas") is None


def test_returns_none_for_empty_message():
    assert detect_location("") is None


def test_detection_is_case_insensitive():
    assert detect_location("estoy en matagalpa") == "Matagalpa,NI"
    assert detect_location("LEON tiene mucho calor") == "Leon,NI"
