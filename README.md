# ASTROS
Semester 1 Project

## Python Pirates

- Syeda Sana Zehra Zaidi
- Hamna Rauf
- Hamna Naveed
- Muhammad Waseem

## Project Description
    The game revolves around a space expedition in a spacecraft.

    The expedition encounters several challenges like comets, asteroids that need to be shoot down and black holes that need to be avoided to preserve life and to gain points.

    The spacecraft also encounters boosters.

    As the expeditionary force gains points, they enter into higher levels (up to level 4) increasing difficulty.

## Features
   * MAIN MENU ELEMENTS
   
    - Play
    
    - Instructions
    
    - Credits
    
    - Exit

   * BACKGROUND
   
    - Movement of background stars gives perspective of motion of the spacecraft which stays at the center of the screen.
    
   * HEADS-UP DISPLAY
   
    - Health Bar (4 units)
    
    - Score 

   * LEVELS OF DIFFICULTY
   
    - Shifting of levels is success-based.
    
    - Each higher level encompasses a higher level of difficulty with more frequent obstacles.

   * Voice automation
   
    - Background music of menu and game.
    
    - Interaction with boosters and hurdles are marked by different sounds

## Detailed Documentation
   * External Libraries:
   
    - pygame
        Open Command Prompt
        
        Type **'pip install pygame'**

   * Instructions:
    - Movement of Spacecraft: 
      - Up Key: Speeds up
      - Down Key: Slows down
      - Left Key: Turns left
      - Right Key: Turns Right  
      - Spacebar: Shoots bullets
      - Esc Key: Terminates the current game session

    - Power-Ups:
      - Frost Ball:
            Freezes the approaching hurdles
      - Energizer:
            Recuperates the spacecraft

    - Hurdles:
      - Black Hole:
            Cannot be obliterated
            Interaction with it completely damages the spacecraft
      - Large Asteroid:
            Reduces health of spacecraft by three levels
      - Small Asteroid / Comet-I / Comet-II
            Can be destroyed with a single bullet
            Causes a single level damage to the spacecraft
