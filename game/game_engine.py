import random
import pygame
from game.text_box import TextBox


class GameEngine:
    # Task 4: Maximum number of valid attempts
    MAX_ATTEMPTS = 10

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Secret number
        self.secret_number = random.randint(1, 100)

        # Game state
        self.attempts = 0
        self.game_won = False
        self.game_over = False

        # Task 2: Possible range
        self.min_possible = 1
        self.max_possible = 100

        # Task 3: Recent guess history
        self.guess_history = []
        self.max_history = 5

        # Feedback
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        # Input and submit button
        self.input_box = TextBox(
            width // 2 - 110,
            150,
            120,
            48
        )

        self.submit_btn = pygame.Rect(
            width // 2 + 25,
            150,
            100,
            48
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

    def submit_guess(self):
        # Task 4: Stop accepting guesses after game ends
        if self.game_won or self.game_over:
            return

        # Task 1: Prevent empty-input crash
        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number."
            self.feedback_color = (240, 200, 80)
            return

        # Convert input to integer
        guess = int(self.input_box.text)

        # Count valid guesses only
        self.attempts += 1

        # Clear input
        self.input_box.clear()

        # -------------------------
        # CHECK THE GUESS
        # -------------------------

        if guess < self.secret_number:
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

            # Task 2: Narrow lower boundary
            self.min_possible = max(
                self.min_possible,
                guess + 1
            )

            # Task 3: Add guess to history
            self.guess_history.append(
                (guess, "TOO LOW", (80, 160, 240))
            )

        elif guess > self.secret_number:
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

            # Task 2: Narrow upper boundary
            self.max_possible = min(
                self.max_possible,
                guess - 1
            )

            # Task 3: Add guess to history
            self.guess_history.append(
                (guess, "TOO HIGH", (240, 100, 80))
            )

        else:
            # Correct guess
            self.feedback_msg = (
                f"CORRECT! Found in {self.attempts} attempts."
            )
            self.feedback_color = (80, 220, 90)
            self.game_won = True
            self.game_over = True

            # Task 3: Add correct guess to history
            self.guess_history.append(
                (guess, "CORRECT", (80, 220, 90))
            )

        # Keep only the most recent 5 guesses
        if len(self.guess_history) > self.max_history:
            self.guess_history.pop(0)

        # -------------------------
        # TASK 4: GAME OVER
        # -------------------------

        if (
            self.attempts >= self.MAX_ATTEMPTS
            and not self.game_won
        ):
            self.game_over = True

            self.feedback_msg = (
                f"GAME OVER! The number was {self.secret_number}."
            )
            self.feedback_color = (255, 90, 90)

    def reset(self):
        # Generate a new secret number
        self.secret_number = random.randint(1, 100)

        # Reset game state
        self.attempts = 0
        self.game_won = False
        self.game_over = False

        # Task 2: Reset possible range
        self.min_possible = 1
        self.max_possible = 100

        # Task 3: Clear guess history
        self.guess_history = []

        # Reset feedback
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        # Clear input
        self.input_box.clear()

    def handle_event(self, event):
        # Pass event to text box
        self.input_box.handle_event(event)

        # Keyboard events
        if event.type == pygame.KEYDOWN:

            # Enter submits guess
            if event.key == pygame.K_RETURN:
                self.submit_guess()

            # R restarts after winning or losing
            elif (
                event.key == pygame.K_r
                and self.game_over
            ):
                self.reset()

        # Mouse events
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        # Background
        screen.fill((30, 34, 42))

        # -------------------------
        # TITLE
        # -------------------------
        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                35
            )
        )

        # -------------------------
        # ATTEMPTS
        # -------------------------
        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts} / {self.MAX_ATTEMPTS}",
            True,
            (180, 185, 195)
        )

        screen.blit(
            attempts_surf,
            (
                self.width // 2
                - attempts_surf.get_width() // 2,
                90
            )
        )

        # -------------------------
        # TASK 2: POSSIBLE RANGE
        # -------------------------
        range_surf = self.font_medium.render(
            f"Possible range: "
            f"{self.min_possible} - {self.max_possible}",
            True,
            (180, 220, 180)
        )

        screen.blit(
            range_surf,
            (
                self.width // 2
                - range_surf.get_width() // 2,
                120
            )
        )

        # -------------------------
        # INPUT BOX
        # -------------------------
        self.input_box.render(screen)

        # -------------------------
        # SUBMIT BUTTON
        # -------------------------
        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx
                - btn_text.get_width() // 2,
                self.submit_btn.centery
                - btn_text.get_height() // 2
            )
        )

        # -------------------------
        # FEEDBACK
        # -------------------------
        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2
                - feedback_surf.get_width() // 2,
                235
            )
        )

        # -------------------------
        # TASK 3: RECENT GUESS HISTORY
        # -------------------------
        history_title = self.font_small.render(
            "RECENT GUESSES",
            True,
            (245, 245, 245)
        )

        screen.blit(
            history_title,
            (25, 200)
        )

        if not self.guess_history:
            empty_history = self.font_small.render(
                "No guesses yet",
                True,
                (140, 145, 155)
            )

            screen.blit(
                empty_history,
                (25, 225)
            )

        else:
            y_position = 225

            for guess, result, color in self.guess_history:
                history_text = self.font_small.render(
                    f"{guess} -> {result}",
                    True,
                    color
                )

                screen.blit(
                    history_text,
                    (25, y_position)
                )

                y_position += 25

        # -------------------------
        # TASK 4: GAME OVER / WIN
        # -------------------------
        if self.game_over:
            if self.game_won:
                restart_message = (
                    "You won! Press [R] to Start a New Game"
                )
            else:
                restart_message = (
                    "Press [R] to Start a New Game"
                )

            restart_surf = self.font_medium.render(
                restart_message,
                True,
                (255, 220, 80)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    295
                )
            )