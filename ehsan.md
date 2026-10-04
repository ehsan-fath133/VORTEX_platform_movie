# Python Flappy Bird
A simple Flappy Bird clone built with python and pygame

## Table Of Contents
- [Table Of Contents](#table-of-contents)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirement](#requirement)
- [Installation](#installation)
- [Envoirment Setup](#envoirment-setup)
- [Usage](#usage)
- [Example Output](#example-output)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Lincence](#lincence)
- [Aurthor](#aurthor)
## Features
- Flappy Bird Gameplay
  - Bird flaps when the player presses space or left click
  - Pipes move from right to left
  - Collision detection with pipes and ground
  - Score increases when the bird passes a pipe
  - Game over screen with restart option
- Graphics And Sound
  - Simple bird, pipe and background images
  - Optional flap and hit sound effects
- Score System
  - Shows the current score on the screen
  - Saves the high score in `highscore.txt`
- Controls
  - `SPACE` or mouse click to flap
  - `R` to restart after game over
  - `ESC` to quit the game

## Project Structure

```text
python_flappy_bird/
│   main.py
│   game.py
│   assets/
│       bird.png
│       pipe.png
│       background.png
│       base.png
│   highscore.txt
│   requirements.txt
│   .gitignore
│   README.md
```

### File discription
- `main.py` - main file used to run the flappy bird game
- `game.py` - stores game logic, bird, pipes and collision
- `assets/` - folder for images used in the game
- `highscore.txt` - saves the best score of the player
- `requirements.txt` - list of python packages needed by the project
- `.gitignore` - tells git which files and folders should not be tracked
- `README.md` - contains the project documentation

## Requirement
Before running the project, make sure you have:
- `python 3`
- `pygame`

## Installation
1. open a terminal in the project folder.
2. check that python is installed
```bash
python --version
```

3. install the python packages
```bash
pip install -r requirements.txt
```

## Envoirment Setup
This project does not need a `.env` file.

If you want, you can add extra settings later, for example:
- window width and height
- bird speed
- pipe gap size

No secret password or private key is required to play the game.

## Usage
1. open a terminal in the project folder
2. run the game
```bash
python main.py
```
3. press `SPACE` or click to make the bird flap
4. try to fly between the pipes without hitting them
5. after game over, press `R` to play again or `ESC` to exit

## Example Output
When the game starts, a window opens with:
- a bird in the middle of the screen
- green pipes moving toward the bird
- the current score at the top of the screen

Example terminal message:

```text
Flappy Bird started
High score: 12
Press SPACE to flap
```

After the bird hits a pipe:

```text
Game Over
Your score: 7
High score: 12
Press R to restart
```
## Screenshot

## ROADMAP
- [x] add multiple quiz question
- [x] calculate the final score 
- [x] save results to a file 
- [x] add admin mode
- [ ] add more quiz questions
- [ ] add difficultly levels
- [ ] add a timer

## Contributing

## Licence

## Author
create by [mohamad javad]()

