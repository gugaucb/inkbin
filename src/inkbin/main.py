from fastapi import FastAPI

from inkbin.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Inkbin",
    description="Plataforma editorial para compartilhamento anônimo e seguro de código e textos.",
    version="0.1.0",
    debug=settings.DEBUG,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": "inkbin"}
