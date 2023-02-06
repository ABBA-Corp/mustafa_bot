from aiogram import Dispatcher

from .scheduler import SchedulerMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, scheduler):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SchedulerMiddleware(scheduler))
