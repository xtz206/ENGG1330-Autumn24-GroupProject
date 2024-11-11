HOW TO RUN THE GAME

1. Open your terminal.
2. Make sure the size of the terminator's window is the maxnium, otherwise an error may occur.
3. Input python ./src/main.py in your terminal.
4. Press enter and enjoy.

**Please do NOT change the size of your window during the game, otherwise an error may occur.

--------------------------------------------------------------------------------------------------------------------------------------------------

INSTRUCTION OF THE GAME
*You can view the instruction by pressing 't' in the menu, but here we provide a more detailed illustration in case of any problem.

1. Solid_Blocks
    1.1 Player
        
        Player is the only object you may control in the game.

        Player will be showcased as a green block with an '@'.
        
        Player can interact with the following blocks:
            Box, Bonus, Chaser, Exit, Fixed_chaser
        
        To control the player:
            Press 'W' to move up;
            Press 'A' to move left;
            Press 'S' to move down;
            Press 'D' to move right.

        Only after the player's move will other objects move.

    1.2 Box

        Box is an object whose move is determined by player.

        Box will be showcased as a black block with an '#'.

        To move the Box:
            Player should be next to the box and move towards the box;
            The Box will move one step to the same as the direction of the player's move;
            There should be no solid objects on the Box's next position;
            If the block on the next position is NOT solid, Box will hide it until it being moved away;
            *IMPORTANT: To move multiple Boxes at a time is ILLEGAL.
        
        Box's move is the priorest after the player's move.

    1.3 Fixed_chaser
        
        Fixed_chaser is an object who will go in a fixed route, either a circle or a straight round trip.

        Chaser will be showcased as a red block with an 'G';
        A not-solid block with cyan color shows the next position of Fixed_chaser (Also distinguish it from Chaser).

        If chaser reach the player, you will lose at the current map.

        Chaser's move goes after the box's and prior to Chaser's.



    1.4 Chaser (Griever)

        Chaser is an object who will go after the player as close as it can (Using A* algorism).
        
        Chaser will be showcased as a red block with an 'G'.

        If chaser reach the player, you will lose at the current map.

        Chaser's move is always the last one, which means that it could be blocked by other movable objects, excluding the player.

    1.5 Wall

        Wall is the edge of the map where player is NOT allowed to reach.

        Wall will be showcased as a yellow block.

2. Not-solid_blocks
    
    2.1 Air

        Air is a block where any movable block can reach.

        Air will be showcased as a white (or no color) block.

        Basically, all moves should be on Air blocks.

    2.2 Bonus

        Bonus is a block which will add player's score once being reached by player.

        Bonus will be showcases as a green block with an '$'.

        Bonus will disappear after player's reach.

        Bonus can be hidden if a movable block moves to its position.

        Try get as mush Bonus as you can.

    2.3 Exit

        Exit is a block where is the end of each map.

        Exit will be displayed as a green block with 'E'.

        Once player reach the Exit, player wins at the current map.

    2.4 Start

        Start is the initial position of the player.

        Start will be displayed as a green block

3. Other operations

    3.1 Quit
        
        You may press 'q' to quit the game at any time when you play. This will terminate the program and all your operations will NOT be reserved.
    
    3.2 Back to Menu

        You may press 'm' to get back to menu page when you are at:

            Winning page/Losing page/End of the whole game/Any of the map
        
        If you get back to menu in a map, your operations in the map will NOT be reserved.
    
    3.3 Retry

        You may press 'R' to retry in any of the map. This will initialize all objects in the map.

    3.4 Continue

        If you win at a map, you may press 'c' to proceed to the next map.
        (Continue will only be available when there is a hint on your screen)
        
    3.5 Choose a map

        In the menu, you may press a number from 1-9 to jump to any of the maps.
        However we suggest you play from the Tutorial.

    3.6 Tutorial

        In the menu, you may press 't' to start the Tutorial where there is a brief instruction of the game and a tutorial map.

        

