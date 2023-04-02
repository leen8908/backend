from passlib.context import CryptContext
import pytz
import datetime as dt
import multiprocessing


def get_tw_time() -> str:
    tw = pytz.timezone('Asia/Taipei')
    twdt = tw.localize(dt.datetime.now()).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return twdt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def number_of_workers():
    print((multiprocessing.cpu_count() * 2) + 1)
    return (multiprocessing.cpu_count() * 2) + 1