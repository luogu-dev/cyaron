import random
from queue import PriorityQueue
from typing import Union, Sequence, Tuple

from cyaron import IO


def _check_defaults_format(defaults):
    for sub in defaults:
        for args in sub:
            if not isinstance(args, Sequence) or len(args) != 2:
                return False
            name, val = args
            if not isinstance(name, str) or not isinstance(val, int):
                return False
    return True


class Data:
    def __init__(
            self,
            name: str,
            subtask: int = 1,
            num: Union[int, Sequence[int]] = 10,
            checkpoints: Union[int, Sequence[int]] = 0,
            args: Sequence[str] = None,
            static: Union[Sequence[Tuple[str, int]], Sequence[Sequence[Tuple[str, int]]]] = None,
            relations: Sequence[Sequence[str]] = None,
            out_gen: str = None,
    ):
        r"""
        Use it as a iter.In each iteration,
        it will return a IO object and some basic args of the checkpoints
        in a tuple like (io, a, b, n, m).
        For example,it can decide the `n` and `m` of the checkpoint,
        and you can use the IO object to write more infomation like a map with `n` points.

        Args:
            name: the name of this data,
                output file name will be "`{name}{index}.in`" and "`name{index}.out`"
            subtask: the subtask number of this data, default is 1
            num: the number of this data,or the number of each subtask
            checkpoints: number for multi checkpoint,or number of each subtask
            args: args' name like `n`,`m` for each group
            static: static args,or static args for each subtask
            relations: relations between args,
                each relation is a list of args mean [0] < [1] < [2]...,
                if [0] <= [1], you can insert '=' between them.
                For example ['a', '=', 'b', 'c'] mean `a <= b < c`
            out_gen: the shell command to start the output generator,(None to disable)

        Example:

            Have no subtask.Need 5 data.No multi checkpoint.
            0 <= l < mid <= r < 20

            >>> Data(
            >>>     name="test",
            >>>     num=5,
            >>>     static=[('L', 0), ('R', 20)],
            >>>     relations=[["L", "=", "l", "mid", "=", "r", "R"]]
            >>> )


            Have 3 subtask,each subtask has 5 data.Each data has 5 checkpoint.
            For first subtask,0 < n < 20.
            For second subtask,20 < n < 40.For third subtask,40 < n < 60.

            >>> Data(
            >>>     name="test",
            >>>     subtask=3,
            >>>     num=[5, 5, 5],
            >>>     checkpoints=[5, 5, 5],
            >>>     static=[[('MIN', 0), ('MAX', 20)],
            >>>             [('MIN', 20), ('MAX', 40)],
            >>>             [('MIN', 40), ('MAX', 60)]],
            >>>     relations=[["MIN", "n", "MAX"]]
            >>> )

            You can find a real example in the `examples` dir
        """
        self.name = name
        self.subtask = subtask
        self.num = num if isinstance(num, Sequence) else [num] * self.subtask
        self.checkpoints = checkpoints if isinstance(checkpoints, Sequence) \
            else [checkpoints] * self.subtask
        self.args = args if args is not None else []
        if static is None:
            self.static = [[]] * self.subtask
        elif _check_defaults_format(static):
            self.static = static
        elif _check_defaults_format([static]):
            self.static = [static] * self.subtask
        else:
            raise ValueError("static args' format is wrong")
        self.relations = relations if relations is not None else []
        self.relation_map = self._compile_args()

        if len(self.num) != self.subtask:
            raise ValueError("num's length must be equal to subtask")
        if len(self.checkpoints) != self.subtask:
            raise ValueError("checkpoints' length must be equal to subtask")
        if len(self.static) != self.subtask:
            raise ValueError("static's length must be equal to subtask")

        self.index = 1
        self.subtask_index = 1
        self.point_index = 1
        self.checkpoint_index = 1
        self.io = None
        self.out_gen = out_gen

    def _compile_args(self):
        relation_map = {}
        for rel in self.relations:
            can_equal = False
            last = None
            for ele in rel:
                if last is None:
                    if ele != "=":
                        last = ele
                    continue
                if ele == "=":
                    can_equal = True
                    continue
                if ele not in relation_map:
                    relation_map[ele] = []
                if last not in relation_map:
                    relation_map[last] = []
                relation_map[ele].append((last, can_equal, 1))
                relation_map[last].append((ele, can_equal, 0))
                last = ele
                can_equal = False
        return relation_map

    def _gen_args(self) -> Tuple:
        max_val = PriorityQueue()
        min_val = PriorityQueue()
        for name, val in self.static[self.subtask_index - 1]:
            max_val.put((val, name))
            min_val.put((-val, name))
        args = set(self.args)
        values = {}
        max_d = {}
        min_d = {}
        while args:
            while not max_val.empty():
                val, name = max_val.get()
                for ele, can_equal, d in self.relation_map[name]:
                    if d != 1:
                        continue
                    new_val = val - (0 if can_equal else 1)
                    if ele not in max_d or new_val < max_d[ele]:
                        max_d[ele] = new_val
                        max_val.put((new_val, ele))
            while not min_val.empty():
                val, name = min_val.get()
                for ele, can_equal, d in self.relation_map[name]:
                    if d != 0:
                        continue
                    new_val = -val + (0 if can_equal else 1)
                    if ele not in min_d or new_val > min_d[ele]:
                        min_d[ele] = new_val
                        min_val.put((-new_val, ele))
            for name in args:
                if name in max_d and name in min_d:
                    values[name] = random.randint(min_d[name], max_d[name])
                    max_val.put((values[name], name))
                    min_val.put((-values[name], name))
                    break
            else:
                print(min_d, max_d)
                raise RuntimeError("Relations too less to generate args")
            args.remove(name)
        return tuple(values[i] for i in self.args)

    def __iter__(self):
        return self

    def __next__(self):
        if self.subtask_index > self.subtask:
            raise StopIteration
        if self.checkpoint_index == 1:
            if self.io is not None and self.out_gen is not None:
                self.io.output_gen(self.out_gen)
            self.io = IO(file_prefix=self.name, data_id=self.index)
            checkpoint = self.checkpoints[self.subtask_index - 1]
            if checkpoint > 0:
                self.io.input_writeln(checkpoint)
        args_value = self._gen_args()
        self.io.input_writeln(args_value)
        self.checkpoint_index += 1

        if self.checkpoint_index > self.checkpoints[self.subtask_index - 1]:
            self.point_index += 1
            self.index += 1
            self.checkpoint_index = 1
        if self.point_index > self.num[self.subtask_index - 1]:
            self.point_index = 1
            self.subtask_index += 1
        return (self.io,) + args_value
