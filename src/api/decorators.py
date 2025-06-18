from functools import wraps
from typing import Any
import json

from fastapi import HTTPException

from src.init import redis_manager


def cache(expire: int = 10) -> Any:
    def wrapper(f: Any) -> Any:
        # возвращаемые данные могут быть списком или словарём, при несоответствии выдаёт ошибку
        data_iterable = False

        @wraps(f)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            nonlocal data_iterable
            # ключ для редиса состоит из названия ручки и её аргументов простых типов
            custom_kwargs = [
                f"{k}={v}"
                for k, v in kwargs.items()
                if "." not in v.__class__.__module__
            ]
            custom_kwargs = "/?" + "&".join(custom_kwargs) if custom_kwargs else ""
            route_name = f.__module__.split(".")[-1]
            redis_key = f"{route_name}" + custom_kwargs
            print(f"{redis_key=}")
            data_from_cache = await redis_manager.get(redis_key)
            if not data_from_cache:
                print("GOING TO DATABASE")
                data_from_db = await f(*args, **kwargs)
                if not data_from_db:
                    raise HTTPException(404, "Data not found")
                if type(data_from_db) == list:
                    data_iterable = True
                    data_schemas = [d.model_dump() for d in data_from_db]  # type: ignore
                else:
                    data_iterable = False
                    data_schemas = [data_from_db.model_dump()]
                data_json = json.dumps(data_schemas, default=str)
                await redis_manager.set(redis_key, data_json, expire)
                return data_from_db  # type: ignore

            data_dicts = json.loads(data_from_cache)
            print(f"{data_dicts=}")
            return data_dicts if data_iterable else data_dicts[0]

        return inner

    return wrapper


# get_facilities = cache(10)(get_facilities)
