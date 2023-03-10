import asyncio
import json
import uuid
import aiohttp

from data import config


async def create_order(user, order, longitude, latitude, address, comment, scheduler, bot):
    data = {
        "client_requirements": {
            "taxi_class": "courier"
        },
        "items": [
            {
                "cost_currency": "UZS",
                "cost_value": "0",
                "droppof_point": 10,
                "pickup_point": 11,
                "quantity": 1,
                "title": f"#{order}"
            }
        ],
        "route_points": [
            {
                "address": {
                    "coordinates": [
                        float(longitude),
                        float(latitude)
                    ],
                    "comment": f"Mustafa uchun {comment} UZS",
                    "fullname": address
                },
                "contact": {
                     "name": f"{user.name}",
                     "phone": f"{user.phone}"
                },
                "point_id": 10,
                "type": "destination",
                "visit_order": 2,
                "skip_confirmation": True
            },
            {
                "address": {
                    "coordinates": [
                        69.282243,
                        41.290850
                    ],
                    "fullname": "Ташкент, улица Айбека, 44, Mustafa"

                },
                "contact": {
                    "name": "Mustafa",
                    "phone": "+998932325151"
                },
                "skip_confirmation": True,
                "point_id": 11,
                "type": "source",
                "visit_order": 1
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.TAXI}create",
                                headers={"Authorization": f"Bearer {config.TAXI_TOKEN}",
                                         "Accept-Language": "ru",
                                         "Content-Type": "application/json"},
                                params={"request_id": str(uuid.uuid1())},
                                data=json.dumps(data)
                                ) as response:
            res = await response.json()
    await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.TAXI}accept",
                                headers={"Authorization": f"Bearer {config.TAXI_TOKEN}",
                                         "Accept-Language": "ru",
                                         "Content-Type": "application/json"},
                                params={"claim_id": res['id']},
                                data=json.dumps({"version": 1})
                                ) as response:
            resps = await response.json()
    await asyncio.sleep(1)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.TAXI}info/?claim_id={res['id']}",
                                headers={"Authorization": f"Bearer {config.TAXI_TOKEN}",
                                         "Accept-Language": "ru",
                                         "Content-Type": "application/json"},
                                params={"claim_id": res['id']},
                                data=json.dumps({"version": 1})
                                ) as response:
            response = await response.json()

        msg = ""
        if user.lang == "uz":
            msg = f"Buyurtma: #{order}\n" \
                  f"Yetkazib berish narxi {response['pricing']['offer']['price']} so'm"
        if user.lang == "ru":
            msg = f"Заказ: #{order}" \
                  f"Сумма доставки {response['pricing']['offer']['price']} сум"
        if user.lang == "tr":
            msg = f"Sipariş: #{order}" \
                  f"Teslimat miktarı {response['pricing']['offer']['price']} som"
        await bot.send_message(chat_id=user.user_id, text=msg)
    scheduler.remove_job(str(order))
