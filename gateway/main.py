from fastapi import FastAPI, Request, HTTPException
import httpx
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="API Gateway")

MICROSERVICES = {
    "auth": "http://auth-service:8000",
    "event": "http://event-service:8000",
}

merged_openapi = None


@app.on_event("startup")
async def merge_openapi_specs():
    global merged_openapi
    merged = {
        "openapi": "3.0.2",
        "info": {"title": "Unified API", "version": "1.0"},
        "paths": {},
        "components": {"schemas": {}},
    }

    async with httpx.AsyncClient(timeout=5) as client:
        for service_name, url in MICROSERVICES.items():
            try:
                resp = await client.get(f"{url}/openapi.json")
                resp.raise_for_status()
                spec = resp.json()
            except Exception:
                # logowanie braku dostępności serwisu
                print(f"Service {service_name} unavailable during startup")
                continue

            # scalanie ścieżek z prefixem
            for path, data in spec.get("paths", {}).items():
                merged["paths"][f"/{service_name}{path}"] = data

            # scalanie schematów
            components = spec.get("components", {})
            schemas = components.get("schemas", {})
            merged["components"]["schemas"].update(schemas)

    merged_openapi = merged


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in MICROSERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{MICROSERVICES[service]}/{path}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            req = client.build_request(
                method=request.method,
                url=url,
                headers=request.headers.raw,
                content=await request.body()
            )
            resp = await client.send(req)
            return resp.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail=f"{service} service unavailable")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


def custom_openapi():
    return merged_openapi


app.openapi = custom_openapi
