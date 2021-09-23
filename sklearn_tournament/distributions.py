from typing import Callable, List, Optional, Union

import scipy.stats

from sklearn_tournament import commons


class ScistatsNormBetween:
    def __init__(
        self,
        small: float,
        large: float,
        cond: Optional[Callable[[float], bool]] = None,
        div: float = 2,
        toint: bool = False,
        clip: bool = False,
        hardClip: bool = False,
    ) -> None:
        def _no_cond(x):
            return True

        def _hard_clip(x):
            return small < x < large

        def _soft_clip(x):
            return small <= x <= large

        #
        self.lower = small
        self.upper = large
        #
        if cond is None:
            cond = _no_cond
        #
        if clip:
            if hardClip:
                clip_cond = _hard_clip
            else:
                clip_cond = _soft_clip
        else:
            clip_cond = _no_cond

        #
        def _cond(x):
            return cond(x) and clip_cond(x)

        self.cond = _cond
        self.norm = scipy.stats.norm(
            loc=(large + small) / 2, scale=(large - small) / (div * 2)
        )
        self.toint = toint

    def _one_rvs(self, *args, **kwargs) -> float:
        while True:
            r = self.norm.rvs(*args, **kwargs)
            if self.toint:
                r = commons.iround(r)
            if self.cond(r):
                break
        return r

    def _many_rvs(self, size: int, *args, **kwargs) -> List[float]:
        return [self._one_rvs(*args, **kwargs) for i in range(size)]

    def rvs(self, size: int = 1, *args, **kwargs) -> Union[float, List[float]]:
        if size > 1:
            return self._many_rvs(size, *args, **kwargs)
        else:
            return self._one_rvs(*args, **kwargs)


class ScistatsNormAround(ScistatsNormBetween):
    def __init__(
        self,
        center: float,
        dist: float,
        cond: Optional[Callable[[float], bool]] = None,
        div: float = 2,
        toint: bool = False,
        clip: bool = False,
        hardClip: bool = False,
    ) -> None:
        super(ScistatsNormAround, self).__init__(
            center - dist, center + dist, cond, div, toint, clip, hardClip
        )
