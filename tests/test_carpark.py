import pytest

from main import getCarparkAvail

@pytest.mark.asyncio(asycio_mode="strict")
async def test_getCarparkAvailNone():
    data = await getCarparkAvail(None)
    assert "items" in data
