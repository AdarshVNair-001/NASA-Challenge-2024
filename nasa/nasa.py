import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
window_width = 1400
window_height = 700
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('NASA SPACE GAME')

# Load and scale the background image (space background)
background_image = pygame.image.load('space_image.jpg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Load the character image (astronaut)
character_image = pygame.image.load('character_image.png')
desired_char_width = 100  # Set your desired width
desired_char_height = 100  # Set your desired height
character_image = pygame.transform.scale(character_image, (desired_char_width, desired_char_height))

# Load NPC image
npc_image = pygame.image.load('npc_image.png')  # Load your NPC image
npc_image = pygame.transform.scale(npc_image, (100, 100))  # Resize NPC image

# Load heart image for health display
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Load moon surface image
moon_surface_image = pygame.image.load('moon_surface_image.png')
moon_surface_image = pygame.transform.scale(moon_surface_image, (window_width, 100))  # Scale it to fit the window width

# Load images for Space Rover section
shuttle_image = pygame.image.load('space_shuttle.png')  # Shuttle image
asteroid_image_r = pygame.image.load('asteroid.png')
space_background_r = pygame.image.load('space_image2.jpg')
play_button_image_r = pygame.image.load('PLAY.png')
hydrogen_cylinder_image = pygame.image.load('hydrogen_cylinder.png')
heart_image_r = pygame.image.load('heart.png')

# Scale down the Space Rover images
space_background_r = pygame.transform.scale(space_background_r, (800, 400))
shuttle_width, shuttle_height = shuttle_image.get_size()
shuttle_image = pygame.transform.scale(shuttle_image, (shuttle_width // 5, shuttle_height // 5))
asteroid_image_r = pygame.transform.scale(asteroid_image_r, (asteroid_image_r.get_width() // 5, asteroid_image_r.get_height() // 5))
hydrogen_cylinder_image = pygame.transform.scale(hydrogen_cylinder_image, (hydrogen_cylinder_image.get_width() // 9, hydrogen_cylinder_image.get_height() // 9))
heart_image_r = pygame.transform.scale(heart_image_r, (heart_image_r.get_width() // 14, heart_image_r.get_height() // 14))
play_button_image_r = pygame.transform.scale(play_button_image_r, (200, 80))  # Adjust size as needed

# Character initial position
char_width, char_height = character_image.get_size()
char_x = window_width // 6
char_y = window_height - char_height - 100  # Adjusted for moon surface

# Character movement variables
velocity = 5  # Normal movement speed
sprint_velocity = 8  # Sprint speed
is_jump = False
jump_count = 10  # Adjusted jump height
gravity = 0.6  # Smoother and less floaty gravity
vertical_velocity = 0  # Variable for vertical movement due to gravity
double_jump_available = True  # Double jump is initially available

# Stamina variables
max_stamina = 100
stamina = max_stamina
stamina_depletion_jump = 10  # Stamina decrease per jump
stamina_depletion_sprint = 0.5  # Stamina decrease rate per frame while sprinting
stamina_recovery = 0.5  # Stamina recovery rate
can_jump = True

# Health variables
health = 5  # The number of hearts (max 5)

# Define colors for stamina bar
stamina_bar_color = (0, 255, 0)  # Green
stamina_bar_bg_color = (100, 100, 100)  # Gray background

# Moon surface position (static)
moon_surface_y = window_height - 100  # Fixed position for moon surface

# Asteroid settings
asteroid_image = pygame.image.load('asteroid.png')  # Load asteroid image
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))  # Resize asteroid image
asteroids = []  # List to hold asteroids
asteroid_spawn_time = 2000  # Time in milliseconds between asteroid spawns
last_spawn_time = pygame.time.get_ticks()  # Get the current time in milliseconds

# Timer settings
start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
time_played = 0  # Variable to keep track of time played

# Trivia questions
trivia_questions = [
    {
        "question": "What planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "What does NASA stand for?",
        "options": ["National Aeronautics and Space Administration", "National Aeronautics and Science Association", "National Association of Space Administrators", "None of the above"],
        "answer": "National Aeronautics and Space Administration"
    },
    {
        "question": "Which planet is known for its rings?",
        "options": ["Earth", "Mars", "Saturn", "Jupiter"],
        "answer": "Saturn"
    },
    {
        "question": "Who was the first person to walk on the Moon?",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        "answer": "Neil Armstrong"
    },
    {
        "question":"What is the primary aim of NASA's PLACES project?",
        "options":["To develop new spacecraft technologies", "To engage middle and high school educators in data-rich Earth science learning","To create video games for astronaut training","To conduct research on planetary geology"],
        "answer":"To engage middle and high school educators in data-rich Earth science learning"
    }
    ,
    {
        "question":"What does the galaxy NGC 4694 look like, as observed by the Hubble Space Telescope?",
        "options":["A spiral galaxy with bright arms", "An oval-shaped galaxy with a bright core and reddish-brown dust","A dark galaxy with no visible stars","A rectangular galaxy with multiple cores"],
         "answer":"An oval-shaped galaxy with a bright core and reddish-brown dust"
        
    },
    {
       "question":"What was the focus of the Culturally Inclusive Planetary Engagement workshop held in Boulder, Colorado?",
        "options":[
            " To discuss the future of space tourism",
            " To foster community engagement in planetary science",
            " To train astronauts for Mars missions",
            " To showcase new satellite technology"
        ],
        "answer": "To foster community engagement in planetary science"
    },
    {
        "question":"What is the significance of the Global Precipitation Measurement (GPM) mission?",
        "options": [
            " It measures the temperature of distant stars",
            " It observes precipitation for scientific and societal benefits",
            " It studies the magnetic fields of planets",
            " It monitors the health of astronauts"
        ],
        "answer": "It observes precipitation for scientific and societal benefits"
    },
    {
        "question":"What was the recent milestone achieved by Gateway's Habitation and Logistics Outpost?",
        "options": [
            " Completion of its first crewed mission",
            " Successful static load testing in Turin, Italy",
            " Launch into lunar orbit",
            " Installation of solar panels"
        ],
        "answer": "Successful static load testing in Turin, Italy"
    },
    {
        "question":"According to new data from NASA's LRO mission, what discovery was made about the lunar surface?",
        "options": [
            " Ice deposits in lunar dust and rock are more extensive than previously thought",
            " There are no ice deposits on the Moon",
            " The Moon's surface is completely dry",
            " Ice can only be found in permanently shadowed regions"
        ],
        "answer": "Ice deposits in lunar dust and rock are more extensive than previously thought"
    },
    {
        "question":"What do the new NASA eClips VALUE Bundles aim to achieve?",
        "options": [
            " To promote space tourism",
            " To provide data for climate change research",
            " To increase STEM literacy and inspire future engineers and scientists",
            " To develop new rocket propulsion technologies"
        ],
        "answer": "To increase STEM literacy and inspire future engineers and scientists"
    },
    {
        "question":"What creative opportunity is being offered at the ASGSR conference in 2024?", 
        "options": [
            " A hackathon for software development",
            " An art competition inviting researchers to showcase their science through art",
            " A documentary film festival",
            " A virtual reality experience for space exploration"
        ],
        "answer": "An art competition inviting researchers to showcase their science through art"
    }
]

# Function to draw the moon surface using an image
def draw_moon_surface():
    screen.blit(moon_surface_image, (0, moon_surface_y))  # Draw the moon surface

# Function to display tutorial text
def show_tutorial():
    font = pygame.font.Font(None, 36)  # Create a font object
    tutorial_texts = [
        "Welcome to NASA Space Game!",
        "Controls:",
        "Arrow Keys: Move Left/Right",
        "Space: Jump",
        "Left Shift: Sprint",
        "Press any key to continue..."
    ]
    
    # Draw the NPC
    screen.blit(npc_image, (window_width // 2 - 50, window_height // 2 - 100))  # Position NPC in the center

    # Draw the tutorial text
    for i, text in enumerate(tutorial_texts):
        rendered_text = font.render(text, True, (255, 255, 255))  # White text
        screen.blit(rendered_text, (50, 100 + i * 40))  # Display text

# Function to draw buttons
def draw_buttons():
    font = pygame.font.Font(None, 48)  # Create a font object
    trivia_button_text = font.render('Trivia', True, (255, 255, 255))  # White text
    run_button_text = font.render('Space Run', True, (255, 255, 255))  # White text
    rover_button_text = font.render('Shuttle Dash', True, (255, 255, 255))  # White text

    # Get rectangles
    trivia_button_rect = trivia_button_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    run_button_rect = run_button_text.get_rect(center=(window_width // 2, window_height // 2 + 10))
    rover_button_rect = rover_button_text.get_rect(center=(window_width // 2, window_height // 2 + 70))

    # Draw buttons
    pygame.draw.rect(screen, (0, 0, 0), trivia_button_rect.inflate(20, 20))  # Button background
    screen.blit(trivia_button_text, trivia_button_rect)  # Draw trivia button text

    pygame.draw.rect(screen, (0, 0, 0), run_button_rect.inflate(20, 20))  # Button background
    screen.blit(run_button_text, run_button_rect)  # Draw run button text

    pygame.draw.rect(screen, (0, 0, 0), rover_button_rect.inflate(20, 20))  # Button background
    screen.blit(rover_button_text, rover_button_rect)  # Draw rover button text

    return trivia_button_rect, run_button_rect, rover_button_rect  # Return rectangles for button checking

# Function to handle trivia questions
def trivia_game():
    global running
    score = 0  # Initialize score
    total_questions = len(trivia_questions)
    random.shuffle(trivia_questions)  # Shuffle questions

    for question in trivia_questions:
        question_text = question["question"]
        options = question["options"]
        correct_answer = question["answer"]

        # Display question and options
        font = pygame.font.Font(None, 36)  # Create a font object
        screen.fill((0, 0, 0))  # Clear screen
        rendered_question = font.render(question_text, True, (255, 255, 255))  # White text
        screen.blit(rendered_question, (50, 50))  # Display question

        # Display options
        for i, option in enumerate(options):
            rendered_option = font.render(f"{i + 1}. {option}", True, (255, 255, 255))  # White text
            screen.blit(rendered_option, (50, 100 + i * 40))  # Display options

        pygame.display.flip()  # Update the display

        answered = False  # Flag to check if the question has been answered
        while not answered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        answer_index = event.key - pygame.K_1  # Get index based on key pressed
                        if options[answer_index] == correct_answer:
                            score += 1  # Increase score for correct answer
                        answered = True  # Move to the next question

        pygame.time.wait(1000)  # Wait before showing the next question

    # Show score after all questions
    screen.fill((0, 0, 0))  # Clear screen
    rendered_score = font.render(f"Your score: {score}/{total_questions}", True, (255, 255, 255))  # White text
    screen.blit(rendered_score, (window_width // 2 - 100, window_height // 2 - 20))  # Display score
    pygame.display.flip()  # Update the display
    pygame.time.wait(3000)  # Wait before returning to the main menu

# Function to draw timer
def draw_timer(time_played):
    font = pygame.font.Font(None, 36)  # Create a font object
    timer_text = font.render(f'Time: {time_played // 1000}s', True, (255, 255, 255))  # White text
    screen.blit(timer_text, (window_width - 200, 10))  # Display the timer at the top right

# Function for game over screen
def game_over_screen(time_played):
    font = pygame.font.Font(None, 48)  # Create a font object
    screen.fill((0, 0, 0))  # Clear screen
    game_over_text = font.render('Game Over', True, (255, 0, 0))  # Red text
    time_played_text = font.render(f'Time Played: {time_played // 1000} seconds', True, (255, 255, 255))  # White text
    screen.blit(game_over_text, (window_width // 2 - 100, window_height // 2 - 40))  # Display game over text
    screen.blit(time_played_text, (window_width // 2 - 150, window_height // 2 + 20))  # Display time played

    # Restart and exit buttons
    restart_text = font.render('Restart', True, (255, 255, 255))
    exit_text = font.render('Exit', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 100))
    exit_rect = exit_text.get_rect(center=(window_width // 2, window_height // 2 + 160))
    
    # Draw buttons
    pygame.draw.rect(screen, (0, 0, 0), restart_rect.inflate(20, 20))  # Button background
    screen.blit(restart_text, restart_rect)  # Draw restart button text
    pygame.draw.rect(screen, (0, 0, 0), exit_rect.inflate(20, 20))  # Button background
    screen.blit(exit_text, exit_rect)  # Draw exit button text

    pygame.display.flip()  # Update display
    return restart_rect, exit_rect  # Return rectangles for button checking

# Function to check for collisions
def check_collisions(char_rect):
    global health
    for asteroid in asteroids:
        if char_rect.colliderect(pygame.Rect(asteroid.x, asteroid.y, 50, 50)):
            health -= 1  # Decrease health on collision
            asteroids.remove(asteroid)  # Remove the asteroid
            break  # Exit the loop after collision

# Class for asteroids
class Asteroid:
    def __init__(self):
        self.size = 50  # Set asteroid size
        self.x = random.randint(0, window_width - self.size)  # Random x position
        self.y = -self.size  # Start above the screen
        self.speed = random.uniform(2, 5)  # Random speed

    def update(self):
        self.y += self.speed  # Move asteroid down

    def draw(self):
        screen.blit(asteroid_image, (self.x, self.y))  # Draw asteroid

# ==================== Space Rover Section ====================

def space_rover_game():
    import pygame
    import random
    import sys

    # Initialize Pygame 

    # Set up display
    WINDOW_WIDTH_R = 800
    WINDOW_HEIGHT_R = 400
    screen_r = pygame.display.set_mode((WINDOW_WIDTH_R, WINDOW_HEIGHT_R))
    pygame.display.set_caption('Space Rover')  # Game title

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Load images (already loaded above, reuse if possible)
    # shuttle_image, asteroid_image_r, space_background_r, play_button_image_r, hydrogen_cylinder_image, heart_image_r

    # Create masks for collision detection
    shuttle_mask = pygame.mask.from_surface(shuttle_image)

    # Frame rate
    FPS_R = 50
    clock_r = pygame.time.Clock()

    # Shuttle properties
    shuttle_x_r = (WINDOW_WIDTH_R - shuttle_image.get_width()) // 2
    shuttle_y_r = WINDOW_HEIGHT_R // 2
    vertical_velocity_r = 0
    gravity_force_r = 0.2

    # Obstacle and hydrogen cylinder properties
    obstacles_r = []
    hydrogen_cylinders_r = []
    hearts_r = []
    spawn_timer_r = 0
    hydrogen_spawn_timer_r = 29
    heart_spawn_chance_r = 10
    obstacle_speed_r = 2

    # Oxygen level
    oxygen_level_r = 100
    oxygen_depletion_rate_r = 0.1
    hydrogen_refill_amount_r = 80

    # Life counter
    lives_r = 5

    # Score
    score_r = 0
    font_r = pygame.font.SysFont(None, 30)

    # Game state variables
    game_over_r = False
    game_started_r = False

    # High score reset to 0 at the beginning of each run
    high_score_r = 0  

    # Functions to generate obstacles
    def create_obstacle_r():
        height_offset = random.randint(0, WINDOW_HEIGHT_R - asteroid_image_r.get_height())
        return pygame.Rect(WINDOW_WIDTH_R, height_offset, asteroid_image_r.get_width(), asteroid_image_r.get_height())

    # Functions to generate hydrogen cylinders
    def create_hydrogen_cylinder_r():
        height_offset = random.randint(0, WINDOW_HEIGHT_R - hydrogen_cylinder_image.get_height())
        return pygame.Rect(WINDOW_WIDTH_R, height_offset, hydrogen_cylinder_image.get_width(), hydrogen_cylinder_image.get_height())

    # Function to generate hearts
    def create_heart_r():
        height_offset = random.randint(0, WINDOW_HEIGHT_R - heart_image_r.get_height())
        return pygame.Rect(WINDOW_WIDTH_R, height_offset, heart_image_r.get_width(), heart_image_r.get_height())

    # Function to draw text
    def draw_text_r(text, font, color, x, y):
        screen_text = font.render(text, True, color)
        screen_r.blit(screen_text, [x, y])

    # Function to reset game
    def reset_game_r():
        nonlocal shuttle_x_r, shuttle_y_r, vertical_velocity_r, score_r, obstacles_r, spawn_timer_r, game_over_r, oxygen_level_r, hydrogen_cylinders_r, hearts_r, lives_r
        shuttle_x_r = (WINDOW_WIDTH_R - shuttle_image.get_width()) // 2
        shuttle_y_r = WINDOW_HEIGHT_R // 2
        vertical_velocity_r = 0
        score_r = 0
        oxygen_level_r = 100
        obstacles_r = []
        hydrogen_cylinders_r = []
        hearts_r = []
        spawn_timer_r = 0
        lives_r = 5
        game_over_r = False

    # Function to draw the oxygen bar
    def draw_oxygen_bar_r(oxygen_level):
        bar_x = 10
        bar_y = 80
        bar_width = 20
        bar_height = 200
        fill_height = (oxygen_level / 100) * bar_height

        pygame.draw.rect(screen_r, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        pygame.draw.rect(screen_r, GREEN, (bar_x, bar_y + (bar_height - fill_height), bar_width, fill_height))

    # Function to draw hearts
    def draw_hearts_r(lives):
        for i in range(lives):
            screen_r.blit(heart_image_r, (WINDOW_WIDTH_R - (i + 1) * (heart_image_r.get_width() + 5), 10))

    # Main game loop for Space Rover
    running_r = True
    background_x_r = 0
    background_speed_r = 0.3

    while running_r:
        clock_r.tick(FPS_R)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over_r:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game_r()

            if not game_started_r:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    play_button_rect_r = play_button_image_r.get_rect(center=(WINDOW_WIDTH_R // 2, WINDOW_HEIGHT_R // 2))
                    if play_button_rect_r.collidepoint(mouse_pos):
                        game_started_r = True

        if not game_started_r:
            screen_r.blit(space_background_r, (0, 0))
            play_button_rect_r = play_button_image_r.get_rect(center=(WINDOW_WIDTH_R // 2, WINDOW_HEIGHT_R // 2))
            screen_r.blit(play_button_image_r, play_button_rect_r.topleft)
            pygame.display.update()
            continue

        if not game_over_r:
            background_x_r -= background_speed_r
            if background_x_r <= -space_background_r.get_width():
                background_x_r = 0

            keys_r = pygame.key.get_pressed()
            if keys_r[pygame.K_SPACE]:
                vertical_velocity_r = -3
            else:
                vertical_velocity_r += gravity_force_r

            shuttle_y_r += vertical_velocity_r

            if shuttle_y_r <= 0:
                shuttle_y_r = 0
                vertical_velocity_r = 0
            elif shuttle_y_r >= WINDOW_HEIGHT_R - shuttle_image.get_height():
                shuttle_y_r = WINDOW_HEIGHT_R - shuttle_image.get_height()
                vertical_velocity_r = 0
                game_over_r = True

            if spawn_timer_r <= 0:
                obstacles_r.append(create_obstacle_r())
                if random.randint(0, hydrogen_spawn_timer_r) < 5:
                    hydrogen_cylinders_r.append(create_hydrogen_cylinder_r())
                if random.randint(0, 100) < heart_spawn_chance_r:
                    hearts_r.append(create_heart_r())
                spawn_timer_r = 60

            spawn_timer_r -= 1

            for obstacle in obstacles_r:
                obstacle.x -= obstacle_speed_r
                if obstacle.x < 0:
                    obstacles_r.remove(obstacle)

            for cylinder in hydrogen_cylinders_r:
                cylinder.x -= obstacle_speed_r
                if cylinder.x < 0:
                    hydrogen_cylinders_r.remove(cylinder)

            for heart in hearts_r:
                heart.x -= obstacle_speed_r
                if heart.x < 0:
                    hearts_r.remove(heart)

            shuttle_rect_r = pygame.Rect(shuttle_x_r, shuttle_y_r, shuttle_image.get_width(), shuttle_image.get_height())
            for obstacle in obstacles_r:
                obstacle_mask_r = pygame.mask.from_surface(asteroid_image_r)
                offset_r = (obstacle.x - shuttle_x_r, obstacle.y - shuttle_y_r)
                if shuttle_mask.overlap(obstacle_mask_r, offset_r):
                    lives_r -= 1
                    obstacles_r.remove(obstacle)
                    if lives_r <= 0:
                        game_over_r = True
                    break

            for cylinder in hydrogen_cylinders_r:
                if shuttle_rect_r.colliderect(cylinder):
                    oxygen_level_r += hydrogen_refill_amount_r
                    hydrogen_cylinders_r.remove(cylinder)
                    if oxygen_level_r > 100:
                        oxygen_level_r = 100

            for heart in hearts_r:
                if shuttle_rect_r.colliderect(heart) and lives_r < 5:
                    lives_r += 1
                    hearts_r.remove(heart)
                    break

            oxygen_level_r -= oxygen_depletion_rate_r
            if oxygen_level_r <= 0:
                game_over_r = True

            # Spawn hydrogen cylinder if oxygen level drops below threshold
            if oxygen_level_r < 35 and spawn_timer_r <= 0:
                hydrogen_cylinders_r.append(create_hydrogen_cylinder_r())

            # Update score and handle speed increase
            score_r += 1
            if score_r > high_score_r:
                high_score_r = score_r
            if score_r % 1000 == 0:
                obstacle_speed_r += 2
                hydrogen_spawn_timer_r += 2

            # Draw everything
            screen_r.blit(space_background_r, (background_x_r, 0))
            screen_r.blit(space_background_r, (background_x_r + space_background_r.get_width(), 0))
            screen_r.blit(shuttle_image, (shuttle_x_r, shuttle_y_r))

            for obstacle in obstacles_r:
                screen_r.blit(asteroid_image_r, obstacle.topleft)
            for cylinder in hydrogen_cylinders_r:
                screen_r.blit(hydrogen_cylinder_image, cylinder.topleft)
            for heart in hearts_r:
                screen_r.blit(heart_image_r, heart.topleft)

            draw_text_r(f'Score: {score_r}', font_r, WHITE, 10, 10)
            draw_text_r(f'High Score: {high_score_r}', font_r, WHITE, 10, 30)
            draw_oxygen_bar_r(oxygen_level_r)
            draw_hearts_r(lives_r)

            pygame.display.update()

        if game_over_r:
            screen_r.fill(BLACK)
            draw_text_r('Game Over', font_r, RED, WINDOW_WIDTH_R // 2 - 50, WINDOW_HEIGHT_R // 2 - 20)
            draw_text_r('Press R to Restart', font_r, WHITE, WINDOW_WIDTH_R // 2 - 70, WINDOW_HEIGHT_R // 2 + 10)
            pygame.display.update()

# ==================== End of Space Rover Section ====================

# Function to handle Space Rover
def handle_space_rover():
    space_rover_game()

# Function to draw the main menu
def main_menu():
    screen.blit(background_image, (0, 0))  # Draw background
    trivia_button_rect, run_button_rect, rover_button_rect = draw_buttons()  # Get button rectangles

    # Check for mouse clicks on buttons
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if run_button_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Space Run button pressed
        return 'gameplay'  # Change state to gameplay

    elif trivia_button_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Trivia button pressed
        trivia_game()  # Start trivia game

    elif rover_button_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Space Rover button pressed
        handle_space_rover()  # Start Space Rover game
        # After Space Rover game ends, return to main menu
        return 'main_menu'

    return 'main_menu'

# Function to check for collisions in Space Run
# (Already defined above)

# Main game loop
running = True
game_state = 'main_menu'  # Set initial game state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == 'main_menu':
        game_state = main_menu()

    elif game_state == 'gameplay':
        # Clear the screen and redraw background
        screen.blit(background_image, (0, 0))  # Draw background for gameplay

        time_played = pygame.time.get_ticks() - start_time  # Calculate time played in milliseconds

        # Check if health is below zero
        if health <= 0:
            game_state = 'game_over'  # Change state to game over
        else:
            # Character movement logic
            keys = pygame.key.get_pressed()
            is_sprinting = keys[pygame.K_LSHIFT] and stamina > 0  # Check if sprinting is allowed
            current_velocity = sprint_velocity if is_sprinting else velocity  # Use sprint speed if sprinting

            # Keep the character within the window boundaries
            if keys[pygame.K_LEFT]:
                char_x -= current_velocity  # Move left
            if keys[pygame.K_RIGHT]:
                char_x += current_velocity  # Move right

            # Ensure character stays within the window
            if char_x < 0:
                char_x = 0
            elif char_x > window_width - char_width:
                char_x = window_width - char_width

            # Jumping Logic
            if not is_jump:
                if keys[pygame.K_SPACE] and can_jump and stamina > 0:  # Start jump if space is pressed and stamina allows
                    is_jump = True
                    vertical_velocity = -jump_count  # Set initial jump velocity
                    stamina -= stamina_depletion_jump  # Reduce stamina
                    if stamina <= 0:  # If stamina is depleted, prevent jumping
                        stamina = 0
                        can_jump = False
            else:
                # Apply gravity to make the character fall back down
                char_y += vertical_velocity  # Move the character based on velocity
                vertical_velocity += gravity  # Gravity pulls the character down

                # Double Jump Logic
                if keys[pygame.K_SPACE] and double_jump_available and vertical_velocity > 0 and stamina > 0:
                    vertical_velocity = -jump_count  # Reset vertical velocity for double jump
                    double_jump_available = False  # Disable double jump after using it
                    stamina -= stamina_depletion_jump  # Reduce stamina again for double jump

                # Check if the character has landed on the moon surface
                if char_y >= moon_surface_y - char_height:  # Adjusted to check landing
                    char_y = moon_surface_y - char_height  # Snap character to moon surface
                    is_jump = False  # Reset jump status
                    vertical_velocity = 0  # Reset vertical velocity
                    double_jump_available = True  # Reset double jump

            # Update asteroids
            if pygame.time.get_ticks() - last_spawn_time > asteroid_spawn_time:
                asteroids.append(Asteroid())  # Create a new asteroid
                last_spawn_time = pygame.time.get_ticks()  # Update last spawn time

            for asteroid in asteroids[:]:  # Create a shallow copy of asteroids list
                asteroid.update()  # Update each asteroid
                if asteroid.y > window_height:  # Remove asteroid if it goes off the screen
                    asteroids.remove(asteroid)

            # Check for collisions with asteroids
            check_collisions(pygame.Rect(char_x, char_y, char_width, char_height))

            # Draw the moon surface
            draw_moon_surface()

            # Draw the character
            screen.blit(character_image, (char_x, char_y))  # Draw character at updated position

            # Draw asteroids
            for asteroid in asteroids:
                asteroid.draw()  # Draw each asteroid

            # Draw health display
            for i in range(health):
                screen.blit(heart_image, (10 + i * 40, 10))  # Draw hearts for health

            # Draw stamina bar
            pygame.draw.rect(screen, stamina_bar_bg_color, (10, 50, 200, 20))  # Background
            pygame.draw.rect(screen, stamina_bar_color, (10, 50, (stamina / max_stamina) * 200, 20))  # Stamina bar

            # Stamina recovery logic
            if not is_sprinting and stamina < max_stamina:
                stamina += stamina_recovery  # Recover stamina over time
                if stamina > max_stamina:
                    stamina = max_stamina  # Cap stamina at maximum

            # Draw the timer
            draw_timer(time_played)  # Show the timer

    elif game_state == 'game_over':
        # Show game over screen with played time
        restart_rect, exit_rect = game_over_screen(time_played)

        # Check for mouse clicks on restart or exit
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if restart_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Restart game
            # Reset all variables for a new game
            char_x = window_width // 6
            char_y = window_height - char_height - 100
            health = 5
            stamina = max_stamina
            start_time = pygame.time.get_ticks()  # Reset timer
            asteroids.clear()  # Clear asteroids
            game_state = 'gameplay'  # Change state back to gameplay

        elif exit_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Exit game
            running = False

    # Update the display
    pygame.display.flip()

    # Set frame rate
    pygame.time.Clock().tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()
sys.exit()


