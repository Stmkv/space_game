import asyncio
import curses
import time

TIC_TIMEOUT = 0.1


# def get_stars(canvas):
#     row, column = (3, 10)
#     while True:
#         canvas.addstr(row, column, "*", curses.A_DIM)
#         canvas.refresh()
#         time.sleep(2)
#         canvas.addstr(row, column, "*")
#         canvas.refresh()
#         time.sleep(0.3)
#         canvas.addstr(row, column, "*", curses.A_BOLD)
#         canvas.refresh()
#         time.sleep(0.5)
#         canvas.addstr(row, column, "*")
#         canvas.refresh()
class EventLoopCommand:
    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):
    def __init__(self, seconds):
        self.seconds = seconds


async def blink(canvas, row, column, symbol="*"):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
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
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()
    # canvas.addstr(row, column, "PRESS START", curses.A_BOLD | curses.A_REVERSE)
    canvas.refresh()
    stars = [
        blink(canvas, row, column + number_column * 2) for number_column in range(5)
    ]
    coroutines = stars
    while True:
        try:
            for coroutine in coroutines.copy():
                sleep_command = coroutine.send(None)
                seconds_to_sleep = sleep_command.seconds
                canvas.refresh()
            time.sleep(seconds_to_sleep)
        except StopIteration:
            coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
