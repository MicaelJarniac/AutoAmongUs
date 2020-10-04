from typing import Tuple


def get_pos(target: Tuple[float, ...], area: Tuple[int, ...]) -> Tuple[int, ...]:
    """Get absolute position, given relative position and target area

    Parameters
    ----------
    target : Tuple[float, float]
        Relative position
    area : Tuple[int, int]
        Absolute area

    Returns
    -------
    Tuple[int, int]
        Absolute position
    """

    return tuple(int(a * b) for a, b in zip(target, area))
