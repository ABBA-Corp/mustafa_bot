import os
import django
from aiogram import Bot, Dispatcher
import logging
import sentry_sdk
from data import config


async def on_startup(dp):
    from utils.set_bot_commands import set_default_commands
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "core.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()
     sentry_sdk.init(
        dsn=config.SENTRY_DSN,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
