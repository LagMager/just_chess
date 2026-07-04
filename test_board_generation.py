"""
Quick manual smoke test for BoardGenerator.
Run directly: python test_board_generation.py

Not a pytest/unittest suite on purpose -- just prints the board
and checks the basic invariants so you can eyeball it fast.
"""

from game.board.generator import BoardGenerator
from game.board.position import Position

POINT_VALUES = set(BoardGenerator.POINT_VALUES)
ENERGY_VALUES = set(BoardGenerator.ENERGY_VALUES)


def print_board(board, spawn_positions):
    spawn_set = {(p.row, p.column) for p in spawn_positions}

    print(f"\nBoard {board.SIZE}x{board.SIZE}")
    header = "    " + " ".join(f"{c:>3}" for c in range(board.SIZE))
    print(header)

    for row in range(board.SIZE):
        cells = []
        for col in range(board.SIZE):
            tile = board.get_tile(Position(row, col))

            if (row, col) in spawn_set:
                cell = " S "
            elif tile.points:
                cell = f"P{tile.points}"
            elif tile.energy:
                cell = f"E{tile.energy}"
            else:
                cell = " . "
            cells.append(f"{cell:>3}")
        print(f"{row:>2}: " + " ".join(cells))

    print("\nLegend: P<n> = point tile, E<n> = energy tile, S = spawn, . = empty\n")


def check_invariants(board, spawn_positions):
    errors = []

    all_tiles = [
        board.get_tile(Position(r, c))
        for r in range(board.SIZE)
        for c in range(board.SIZE)
    ]

    point_tiles = [t for t in all_tiles if t.points]
    energy_tiles = [t for t in all_tiles if t.energy]

    # Counts
    if len(point_tiles) != BoardGenerator.NUM_POINTS:
        errors.append(
            f"Expected {BoardGenerator.NUM_POINTS} point tiles, got {len(point_tiles)}"
        )
    if len(energy_tiles) != BoardGenerator.NUM_ENERGY:
        errors.append(
            f"Expected {BoardGenerator.NUM_ENERGY} energy tiles, got {len(energy_tiles)}"
        )

    # Value uniqueness / correctness
    point_values = [t.points for t in point_tiles]
    if set(point_values) != POINT_VALUES or len(point_values) != len(set(point_values)):
        errors.append(
            f"Point values wrong/duplicated: {sorted(point_values)} vs expected {sorted(POINT_VALUES)}"
        )

    energy_values = [t.energy for t in energy_tiles]
    if set(energy_values) != ENERGY_VALUES or len(energy_values) != len(
        set(energy_values)
    ):
        errors.append(
            f"Energy values wrong/duplicated: {sorted(energy_values)} vs expected {sorted(ENERGY_VALUES)}"
        )

    # No tile is both point and energy
    overlap = [t for t in all_tiles if t.points and t.energy]
    if overlap:
        errors.append(f"{len(overlap)} tiles have BOTH points and energy set")

    # Spawn positions must land on empty tiles
    for pos in spawn_positions:
        tile = board.get_tile(pos)
        if tile.points or tile.energy:
            errors.append(
                f"Spawn position {pos} is not empty (points={tile.points}, energy={tile.energy})"
            )

    # Spawn positions must be distinct
    if len({(p.row, p.column) for p in spawn_positions}) != len(spawn_positions):
        errors.append("Spawn positions are not unique")

    # No consumed tiles at generation time
    consumed = [t for t in all_tiles if t.consumed]
    if consumed:
        errors.append(f"{len(consumed)} tiles are marked consumed on a fresh board")

    return errors


def main(num_runs: int = 20):
    total_errors = 0

    for i in range(num_runs):
        board, spawn_positions = BoardGenerator.generate()
        errors = check_invariants(board, spawn_positions)

        if errors:
            total_errors += len(errors)
            print(f"--- Run {i}: FAILED ---")
            for e in errors:
                print(f"  ! {e}")
            print_board(board, spawn_positions)
        elif i == 0:
            # Only print the board once, for a visual sanity check
            print(f"--- Run {i}: OK (showing board) ---")
            print_board(board, spawn_positions)

    print(f"\n{num_runs} runs completed, {total_errors} invariant violations found.")
    if total_errors == 0:
        print("All good.")


if __name__ == "__main__":
    main()
