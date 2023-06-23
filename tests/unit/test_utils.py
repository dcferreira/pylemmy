"""Test functions from the utils module."""
from pylemmy.utils import stream_apply


class SwitchObj:
    """Test class with a boolean switch."""

    def __init__(self, switch_id: int, *, status: bool = False):
        """Initialize the switch.

        :param switch_id: Some integer id.
        :param status: The initial status.
        """
        self.switch_id = switch_id
        self.status = status

    def flip(self):
        """Flip the status of the switch."""
        self.status = not self.status
        return self.status


def test_stream_apply():
    """Test for 2 simple results "generators" that always return the same list."""
    switches1 = [SwitchObj(1), SwitchObj(2), SwitchObj(3)]

    def generator1():
        return switches1

    switches2 = [SwitchObj(9), SwitchObj(8)]

    def generator2():
        return switches2

    def callback_flip(x):
        x.flip()

    stream_apply(
        [generator1, generator2],
        [lambda x: x.switch_id] * 2,
        callback_flip,
        limit=len(switches1) + len(switches2),
    )

    for s in switches1:
        assert s.status
    for s in switches2:
        assert s.status
