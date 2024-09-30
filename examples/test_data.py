from cyaron import Data, Vector
from cyaron.vector import VectorRandomMode

# Problem:
# Given a sequence with n element a_1 to a_n.
# You should find the longest substring
# that sum of it don't bigger than m and
# length of it don't bigger than k.

# For 20% of data, 1 <= k <= n < 100, 0 <= m <= 1000
# For 100% of data, 1 <= k <= n < 1000, 0 <= m <= 1000000, 0 <= a_i <= 1000000
# Output: The sum of the longest substring.

for io, n, m, k in Data(
        "test",
        subtask=2,
        num=[4, 16],
        args=["n", "m", "k"],
        static=[[("MIN", 1), ("MAX", 100), ("MMIN", 0), ("MMAX", 1000)],
                [("MIN", 100), ("MAX", 1000), ("MMIN", 1000), ("MMAX", 1000000)]],
        relations=[["MIN", "=", "k", "=", "n", "MAX"], ["MMIN", "=", "m", "=", "MMAX"]],
        # out_gen="path to right program"
):
    io.input_writeln(sum(Vector.random(n, [(0, 10000000)],
                                       VectorRandomMode.unique), []))
