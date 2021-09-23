import math
import statistics

from typing import Any, Optional, Sequence

import rich.pretty
import rich.progress
import rich.traceback

from rich.console import Console
from rich.text import Text

########
# global console for rich
rc = Console()


########


def install_rich(conf: Optional[dict] = None) -> None:
    def get_or_std(c, std, key):
        return c.get(key, std[key])

    std_conf = {
        "pretty": {"indents": True, "max": 2, "expand": True},
        "traceback": {"locals": False},
    }
    if conf is None:
        conf = std_conf
    if (pretty_conf := conf.get("pretty", None)) is not None:
        std = std_conf.get("pretty")
        rich.pretty.install(
            console=rc,
            indent_guides=get_or_std(pretty_conf, std, "indents"),
            max_length=get_or_std(pretty_conf, std, "max"),
            expand_all=get_or_std(pretty_conf, std, "expand"),
        )
    if (trace_conf := conf.get("traceback", None)) is not None:
        std = std_conf.get("traceback")
        rich.traceback.install(
            console=rc, show_locals=get_or_std(trace_conf, std, "locals")
        )


# jam_geomean <- function
# (x,
#  na.rm=TRUE,
#  ...)
# {
#    ## Purpose is to calculate geometric mean while allowing for
#    ## positive and negative values
#    x2 <- mean(log2(1+abs(x))*sign(x));
#    sign(x2)*(2^abs(x2)-1);
# }
# taken from: https://jmw86069.github.io/splicejam/reference/jamGeomean.html
def jam_geomean(seq: Sequence[float]) -> float:
    if not len(seq) > 0:
        raise ValueError(
            "seq must be non-empty sequence of numbers. The jam_geomean of an empty sequence is not defined"
        )
    step1 = [math.log(1 + abs(x), 2) * math.copysign(1, x) for x in seq]
    m = statistics.mean(step1)
    return math.copysign(1, m) * ((2 ** abs(m)) - 1)


def list_compare(a: Any, b: Any) -> bool:
    if type(a) != type(b):
        return False
    if type(a) != list:
        return a == b
    if len(a) != len(b):
        return False
    for a_, b_ in zip(a, b):
        if not list_compare(a_, b_):
            return False
    return True


def iround(num: float) -> int:
    return int(round(num, 0))


def round_to_first_significant(num: float, max_digits: int = 3) -> float:
    return round_to_first_significant_digits(num, 1, max_digits)


def round_to_first_significant_digits(
    num: float, digits: int = 1, max_digits: int = 3
) -> float:
    if not digits >= 1:
        raise ValueError("digits must be 1 or greater")
    if not max_digits >= 0:
        raise ValueError("max must be 0 or greater")
    if round(num, max_digits) == 0:
        return 0.0
    #
    first_sig_digit = 0
    while round(num, first_sig_digit) == 0.0:
        first_sig_digit += 1
    round_to = first_sig_digit + digits - 1
    round_to = max_digits if round_to > max_digits else round_to
    return round(num, round_to)


def ema(x: float, mu: Optional[float] = None, alpha: float = 0.3) -> float:
    # taken from https://github.com/timwedde/rich-utils/blob/master/rich_utils/progress.py
    """
    Exponential moving average: smoothing to give progressively lower
    weights to older values.
    Parameters
    ----------
    x  : float
        New value to include in EMA.
    mu  : float, optional
        Previous EMA value.
    alpha  : float, optional
        Smoothing factor in range [0, 1], [default: 0.3].
        Increase to give more weight to recent values.
        Ranges from 0 (yields mu) to 1 (yields x).
    """
    return x if mu is None else (alpha * x) + (1 - alpha) * mu


class ItemsPerSecondColumn(rich.progress.ProgressColumn):
    max_refresh = 0.5

    def __init__(self):
        super().__init__()
        self.seen = dict()
        self.itemsPS = dict()

    def render(self, task: rich.progress.Task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            self.seen[task.id] = 0
            self.itemsPS[task.id] = 0.0
            return Text("(0.0/s)", style="progress.elapsed")
        if task.finished:
            return Text(
                f"({round_to_first_significant_digits(task.completed / elapsed, 3, 3)}/s)",
                style="progress.elapsed",
            )
        if task.completed == 0:
            self.seen[task.id] = 0
            self.itemsPS[task.id] = 0.0
        if self.seen[task.id] < task.completed:
            self.itemsPS[task.id] = round_to_first_significant_digits(
                ema(
                    round_to_first_significant_digits(task.completed / elapsed, 3, 3),
                    self.itemsPS[task.id],
                ),
                3,
                3,
            )
            self.seen[task.id] = task.completed
        return Text(f"({self.itemsPS[task.id]}/s)", style="progress.elapsed")


class SecondsPerItemColumn(rich.progress.ProgressColumn):
    max_refresh = 0.5

    def __init__(self):
        super().__init__()
        self.seen = dict()
        self.secPerItem = dict()

    def render(self, task: rich.progress.Task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            self.seen[task.id] = 0
            self.secPerItem[task.id] = 0.0
            return Text("(0.0s/item)", style="progress.elapsed")
        if task.finished:
            return Text(
                f"({round_to_first_significant_digits(elapsed / task.completed, 3, 3)}s/item)",
                style="progress.elapsed",
            )
        #
        if task.completed == 0:
            self.seen[task.id] = 0
            self.secPerItem[task.id] = round_to_first_significant_digits(elapsed, 3, 3)
            return Text(f"({self.secPerItem[task.id]}s/item)", style="progress.elapsed")
        #
        if self.seen[task.id] < task.completed:
            self.secPerItem[task.id] = round_to_first_significant_digits(
                ema(
                    round_to_first_significant_digits(elapsed / task.completed, 3, 3),
                    self.secPerItem[task.id],
                ),
                3,
                3,
            )
            self.seen[task.id] = task.completed
        return Text(f"({self.secPerItem[task.id]}s/item)", style="progress.elapsed")


def std_progress(
    console: Optional[rich.console.Console] = None,
) -> rich.progress.Progress:
    if console is None:
        console = rc
    return rich.progress.Progress(
        "[progress.description]{task.description}",
        rich.progress.BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "({task.completed}/{task.total})",
        rich.progress.TimeElapsedColumn(),
        "eta:",
        rich.progress.TimeRemainingColumn(),
        ItemsPerSecondColumn(),
        SecondsPerItemColumn(),
        console=console,
        transient=False,
    )
