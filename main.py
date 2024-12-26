import asyncio
import curses
import random
import time

TIC_TIMEOUT = 0.1


class EventLoopCommand:
    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):
    def __init__(self, seconds):
        self.seconds = seconds


async def blink(canvas, row, column, symbol="*"):
    while True:
        star_flash = random.randint(0, 50)
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(star_flash):
            await Sleep(TIC_TIMEOUT)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await Sleep(TIC_TIMEOUT)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await Sleep(TIC_TIMEOUT)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await Sleep(TIC_TIMEOUT)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()
    max_hight, max_width = canvas.getmaxyx()
    # Генерируем звезды
    stars = [
        blink(
            canvas, random.randint(1, max_hight - 2), random.randint(1, max_width - 2)
        )
        for _ in range(200)
    ]
    while True:
        try:
            for coroutine in stars:
                sleep_command = coroutine.send(None)
                seconds_to_sleep = sleep_command.seconds
                canvas.refresh()
            time.sleep(seconds_to_sleep)
        except StopIteration:
            stars.remove(coroutine)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
