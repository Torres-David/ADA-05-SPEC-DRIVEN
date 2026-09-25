import concurrent.futures
import time
import pytest

from src.handler import CustomerSearchHandler


def test_nfr02_rate_limiting_allows_up_to_30_requests_per_minute():
    """NFR-02: Permite hasta 30 peticiones por minuto por usuario autenticado."""
    handler = CustomerSearchHandler()
    user_id = "authenticated_user_01"

    for i in range(30):
        response = handler.handle({"name": "Carlos", "user_id": user_id})
        assert response["status"] == 200, f"Petición {i + 1} debería haber sido aceptada"

    # La petición 31 debe ser rechazada con código HTTP 429 Too Many Requests
    response_31 = handler.handle({"name": "Carlos", "user_id": user_id})
    assert response_31["status"] == 429
    assert "Too Many Requests" in response_31["message"]
    assert "30 peticiones" in response_31["message"]


def test_nfr02_rate_limiting_is_isolated_per_user():
    """NFR-02: El límite es independiente por usuario autenticado."""
    handler = CustomerSearchHandler()
    user_a = "user_alpha"
    user_b = "user_beta"

    # Agotar cuota para usuario A
    for _ in range(30):
        handler.handle({"name": "Carlos", "user_id": user_a})

    # Usuario A bloqueado
    assert handler.handle({"name": "Carlos", "user_id": user_a})["status"] == 429

    # Usuario B no debe verse afectado
    response_b = handler.handle({"name": "Carlos", "user_id": user_b})
    assert response_b["status"] == 200


def test_nfr01_p95_latency_under_50_concurrent_requests():
    """NFR-01: El percentil 95 (p95) del tiempo de respuesta debe ser <= 300 ms

    bajo una carga sostenida de 50 peticiones concurrentes por segundo.
    """
    handler = CustomerSearchHandler()
    num_requests = 50
    latencies = []

    def make_search_request(index: int):
        start = time.perf_counter()
        resp = handler.handle(
            request_payload={"name": "Carlos"},
            user_id=f"concurrent_bench_user_{index}",
        )
        elapsed = time.perf_counter() - start
        assert resp["status"] == 200
        return elapsed

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_search_request, i) for i in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            latencies.append(future.result())

    assert len(latencies) == num_requests

    # Cálculo del percentil 95 (p95)
    latencies.sort()
    p95_index = int(0.95 * len(latencies))
    p95_latency = latencies[p95_index]

    # Requerimiento: p95 <= 300 ms (0.300 segundos)
    assert p95_latency <= 0.300, f"Latencia p95 esperada <= 300ms, obtenida: {p95_latency * 1000:.2f}ms"
