# Mummy - Coin Collection Game

Navigate the mummy through a challenging maze to collect coins while avoiding deadly traps and a roaming enemy. Built using Python and OpenGL, this game combines smooth grid-based and diagonal movement, dynamic hazards, and escalating levels for a fun arcade-style experience.

---

## Features

- **Grid-based Movement with Diagonal Support:** Move the mummy smoothly in all 8 directions.
- **Random Enemy Movement:** A red mummy moves randomly, creating unpredictable danger.
- **Collectible Coins:** Gather blue coins scattered across the maze to earn points.
- **Death Zones:** Green/red flashing tiles that cause an instant restart if touched.
- **Level Progression:** Difficulty increases as you collect more coins (more death zones appear).
- **Maze Walls:** Fixed black walls block movement, forcing players to plan routes.
- **Pause and Restart:** Clickable buttons to pause, restart, or exit the game at any time.
- **Keyboard & Mouse Input:** Move with **W, A, S, D** (including diagonals with key combos); use mouse for UI controls.
- **Smooth Animations:** Smooth rendering for player and enemy movement.
- **Cross-platform Compatibility:** Works on any system with Python and PyOpenGL installed.

---

## Demo

![WhatsApp Video 2025-06-27 at 23 26 43_bce2221e](https://github.com/user-attachments/assets/ca65315f-69f3-4847-bd01-f43c19fee4ad)


---

## Installation

1. Make sure you have Python 3 installed.
2. Install required libraries:

    ```bash
    pip install PyOpenGL PyOpenGL_accelerate
    ```

3. Run the game:

    ```bash
    python mummy_coin_collection.py
    ```

---

## How to Play

- **Move:** Use **W, A, S, D** to move up, left, down, and right.
- **Diagonal Movement:** Use key combinations like **W+D**, **W+A**, **S+D**, or **S+A** to move diagonally.
- **Pause:** Click the pause button at the top-center.
- **Restart:** Click the restart button at the top-left.
- **Exit:** Click the cross button at the top-right.

Collect coins to increase your score while avoiding the red mummy and dangerous flashing tiles (death zones). The game restarts if you collide with either.

---

## Project Structure

- `mummy_coin_collection.py` — Main game script with rendering, input handling, animations, and game logic.
- Built using OpenGL primitives: points, lines, and color rendering.

---

## Future Enhancements

- Smarter enemy behavior (optional).
- Sound effects and background music.
- Multiple maze levels or themes.
- Scoreboard / high score tracking.
- Power-ups or shields.

---

## Acknowledgments

- Built using [PyOpenGL](http://pyopengl.sourceforge.net/)
- Game concept and implementation inspired by classic coin-collecting arcade games and Mummy maze deluxe game

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributors

- [Maisha-Chowdhury](https://github.com/Maisha-Chowdhury)
- (Seham Al Haque)

- 
