import numpy as np
import pytest
from numpy.testing import assert_almost_equal, assert_raises
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import pairwise_kernels

from ...tools import linear
from .. import MaxMargin


class TestMaxMarginStat:
    @pytest.mark.parametrize(
        "n, obs_stat", [(100, 0.6983550238795532), (200, 0.7026459581729386)]
    )
    @pytest.mark.parametrize("obs_pvalue", [1 / 1000])
    def test_linear_oned(self, n, obs_stat, obs_pvalue):
        np.random.seed(123456789)
        x, y = linear(n, 5)
        stat, pvalue = MaxMargin("Dcorr").test(x, y)

        assert_almost_equal(stat, obs_stat, decimal=2)
        assert_almost_equal(pvalue, obs_pvalue, decimal=2)

    def test_kernstat(self):
        np.random.seed(123456789)
        x, y = linear(100, 1)
        stat, pvalue = MaxMargin("Hsic").test(x, y, auto=False)

        assert_almost_equal(stat, 0.1072, decimal=2)
        assert_almost_equal(pvalue, 1 / 1000, decimal=2)


class TestMaxMarginErrorWarn:
    """Tests errors and warnings."""

    def test_no_indeptest(self):
        # raises error if not indep test
        assert_raises(ValueError, MaxMargin, "abcd")
