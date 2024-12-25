import asyncio
import curses
import time


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


async def blink(canvas, row, column, symbol="*", amount_of_ticks=5):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


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
        for coroutine in coroutines.copy():
            try:
                sleep_command = coroutine.send(None)
                seconds_to_sleep = sleep_command.seconds
                time.sleep(seconds_to_sleep)
                canvas.refresh()

            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        time.sleep(1)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
