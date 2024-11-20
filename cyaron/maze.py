import random

__all__ = ["generate_maze"]


def generate_maze(
    width: int,
    height: int,
    *,
    wall: str = "#",
    way: str = ".",
    start: str = "S",
    end: str = "T",
):
    maze = [[wall for _ in range(width)] for _ in range(height)]

    def carve_passages_from(cx, cy):
        d = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(d)
        for dx, dy in d:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == wall:
                maze[ny][nx] = maze[cy + dy][cx + dx] = way
                carve_passages_from(nx, ny)

    start_x = random.randrange(0, width)
    start_y = random.randrange(0, height)
    maze[start_y][start_x] = start
    carve_passages_from(start_x, start_y)

    end_x, end_y = random.choice([(x, y) for x in range(width)
                                  for y in range(height) if maze[y][x] == way])
    maze[end_y][end_x] = end

    return maze
