import time
import json
from json.decoder import JSONDecodeError
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.api.kroger_api_client import KrogerAPIClient


@pytest.fixture
def mock_token_response():
    return {
        "access_token": "test_token",
        "expires_in": 3600
    }


@pytest.fixture
def mock_httpx_client(mock_token_response):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value=mock_token_response)

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post = AsyncMock(return_value=mock_response)

    return mock_client


@pytest.fixture
def mock_kroger_client():
    return KrogerAPIClient(keyword="milk", location_id="1234")


@pytest.fixture
def mock_product_response():
    return {
        "data": [{"productId": "1", "name": "Milk"}],
        "meta": {"pagination": {"total": 100}}
    }


@pytest.fixture(autouse=True)
def reset_token_cache():
    KrogerAPIClient.token_cache = {"access_token": None, "expires_at": 0}


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_kroger_token_success(mock_client, mock_httpx_client):
    mock_client.return_value = mock_httpx_client

    token = await KrogerAPIClient._get_kroger_token()

    assert token == "test_token"
    assert KrogerAPIClient.token_cache["access_token"] == "test_token"
    assert KrogerAPIClient.token_cache["expires_at"] > time.time()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_kroger_token_unauthorized(mock_client):
    mock_response = AsyncMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.post = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Failed to get access token: Unauthorized"):
        await KrogerAPIClient._get_kroger_token()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_kroger_token_server_error(mock_client):
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.post = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Failed to get access token: Internal Server Error"):
        await KrogerAPIClient._get_kroger_token()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_kroger_token_network_error(mock_client):
    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.post = AsyncMock(side_effect=httpx.HTTPError("Network Error"))

    with pytest.raises(Exception, match="Request error while fetching token: Network Error"):
        await KrogerAPIClient._get_kroger_token()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_kroger_token_invalid_json(mock_client):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(side_effect=JSONDecodeError("Invalid JSON", "", 0))

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.post = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Invalid JSON response"):
        await KrogerAPIClient._get_kroger_token()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
async def test_get_products_success(mock_client, mock_kroger_client, mock_product_response, mock_httpx_client):

    mock_client.return_value = mock_httpx_client

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value=mock_product_response)

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(return_value=mock_response)

    products = await mock_kroger_client._get_products()

    assert products == mock_product_response
    assert len(products["data"]) == 1
    assert products["data"][0]["name"] == "Milk"



@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
@patch.object(KrogerAPIClient, "_get_kroger_token", new_callable=AsyncMock)
async def test_get_products_unauthorized(mock_get_token, mock_client, mock_kroger_client):
    mock_get_token.return_value = "test_token"

    mock_response = AsyncMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Failed to fetch products: Unauthorized"):
        await mock_kroger_client._get_products()



@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
@patch.object(KrogerAPIClient, "_get_kroger_token", new_callable=AsyncMock)
async def test_get_products_server_error(mock_get_token, mock_client, mock_kroger_client):
    mock_get_token.return_value = "test_token"
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Failed to fetch products: Internal Server Error"):
        await mock_kroger_client._get_products()


@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
@patch.object(KrogerAPIClient, "_get_kroger_token", new_callable=AsyncMock)
async def test_get_products_network_error(mock_get_token, mock_client, mock_kroger_client):
    mock_get_token.return_value = "test_token"

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(side_effect=httpx.HTTPError("Network Error"))

    with pytest.raises(Exception, match="Request error while fetching products: Network Error"):
        await mock_kroger_client._get_products()



@pytest.mark.asyncio
@patch("app.api.kroger_api_client.httpx.AsyncClient")
@patch.object(KrogerAPIClient, "_get_kroger_token", new_callable=AsyncMock)
async def test_get_products_invalid_json(mock_get_token, mock_client, mock_kroger_client):
    mock_get_token.return_value = "test_token"
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(side_effect=json.JSONDecodeError("Invalid JSON", "", 0))

    mock_instance = mock_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(return_value=mock_response)

    with pytest.raises(Exception, match="Invalid JSON response"):
        await mock_kroger_client._get_products()
