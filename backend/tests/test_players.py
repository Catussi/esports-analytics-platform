def test_create_and_get_player(client):
    payload = {
        "steam_id": "76561198036987787",
        "nickname": "s1mple",
        "team": "NAVI",
        "is_active": True,
    }

    create_response = client.post("/api/v1/players", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["steam_id"] == payload["steam_id"]
    assert created["nickname"] == payload["nickname"]

    get_response = client.get(f"/api/v1/players/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_create_player_conflict_on_duplicate_steam_id(client):
    payload = {
        "steam_id": "76561197971812216",
        "nickname": "player_a",
    }

    first = client.post("/api/v1/players", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/players", json=payload)
    assert second.status_code == 409


def test_create_match_stats_for_player(client):
    player_response = client.post(
        "/api/v1/players",
        json={"steam_id": "76561197972240652", "nickname": "ZywOo"},
    )
    player_id = player_response.json()["id"]

    stats_payload = {
        "map_name": "de_inferno",
        "team_side": "Counter-Terrorist",
        "match_external_id": 4,
        "kills": 28,
        "deaths": 14,
        "assists": 4,
        "headshots": 16,
        "adr": 98.5,
        "kast": 81.2,
        "rating": 1.45,
        "flank_kills": 3,
        "avg_kill_distance": 501379.18,
    }

    stats_response = client.post(f"/api/v1/players/{player_id}/stats", json=stats_payload)
    assert stats_response.status_code == 201
    stats = stats_response.json()
    assert stats["player_id"] == player_id
    assert stats["map_name"] == "de_inferno"
    assert stats["kills"] == 28

    list_response = client.get(f"/api/v1/players/{player_id}/stats")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert listed["total"] == 1
    assert len(listed["items"]) == 1


def test_delete_player(client):
    create_response = client.post(
        "/api/v1/players",
        json={"steam_id": "76561197975824962", "nickname": "NiKo"},
    )
    player_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/players/{player_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/players/{player_id}")
    assert get_response.status_code == 404
