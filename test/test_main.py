from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Teste do endpoint POST para criar uma parcela
def test_create_parcel():
    # Dados de amostra para criar uma parcela
    parcel_data = {
        "name": "Parcela de Milho",
        "owner": "BRC",
        "geometry": "POLYGON((-46.5745 -23.5635, -46.573 -23.5635, -46.573 -23.562, -46.5745 -23.562, -46.5745 -23.5635))"
    }

    # Envia a requisição POST para o endpoint /parcels
    response = client.post("/parcels", json=parcel_data)

    # Verifica se a resposta tem status 200 OK
    assert response.status_code == 200
    assert response.json()["name"] == parcel_data["name"]
    assert response.json()["owner"] == parcel_data["owner"]
    assert "id" in response.json()  # Verifica se o ID foi gerado corretamente


# Teste do endpoint GET para consultar parcelas com o filtro de bounding box
def test_get_parcels():
    # Defina um bounding box com coordenadas fictícias
    minx, miny, maxx, maxy = -46.575, -23.565, -46.572, -23.560

    # Envia a requisição GET para o endpoint /parcels
    response = client.get(f"/parcels?minx={minx}&miny={miny}&maxx={maxx}&maxy={maxy}")

    # Verifica se a resposta tem status 200 OK
    assert response.status_code == 200

    # Verifica se o retorno é uma lista de parcelas
    parcels = response.json()
    assert isinstance(parcels, list)

    # Verifica se pelo menos uma parcela foi retornada
    if parcels:
        assert "id" in parcels[0]
        assert "name" in parcels[0]
        assert "owner" in parcels[0]


# Teste do caso de não encontrar parcelas para o bounding box fornecido
def test_get_parcels_empty():
    # Defina um bounding box que provavelmente não vai ter parcelas
    minx, miny, maxx, maxy = -46.000, -23.000, -45.000, -22.000

    # Envia a requisição GET para o endpoint /parcels
    response = client.get(f"/parcels?minx={minx}&miny={miny}&maxx={maxx}&maxy={maxy}")

    # Verifica se a resposta tem status 404 e a mensagem de erro correta
    assert response.status_code == 404
    assert response.json() == {"detail": "Nenhuma parcela encontrada."}
