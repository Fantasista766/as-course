from typing import List, Dict, Any

from fastapi import FastAPI, Body, Query
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import uvicorn


app = FastAPI(docs_url=None, redoc_url=None)


hotels: List[Dict[str, Any]] = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
]


@app.get("/hotels", summary="Получить список отелей")
def get_hotels(
    id: int | None = Query(None, description="ID отеля"),
    title: str | None = Query(None, description="Название отеля"),
) -> List[Dict[str, Any]]:
    hotels_: List[Dict[str, Any]] = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels", summary="Создать новый отель")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
        }
    )
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}", summary="Обновить данные об отеле")
def update_hotel(
    hotel_id: int,
    title: str = Body(description="Новое название отеля"),
    name: str = Body(description="Новое имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частично обновить данные об отеле",
    description="Позволяет обновить только некоторые поля отеля, такие как название или имя.",
)
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(None, description="Новое название отеля"),
    name: str | None = Body(None, description="Новое имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Hotel not found"}, 404


@app.delete("/hotels/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(
    app.swagger_ui_oauth2_redirect_url or "/docs/oauth2-redirect",
    include_in_schema=False,
)
def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
