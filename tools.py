import pygame

class Timer:
    def __init__(self, seconds, callback, loop=False):
        """
        Initialize the Timer.

        :param seconds: Time in seconds after which the callback is triggered.
        :param callback: Function to execute when the timer ends.
        :param loop: Whether the timer should restart after finishing.
        """
        self.seconds = seconds
        self.callback = callback
        self.loop = loop
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        """Start or resume the timer."""
        if not self.running:
            self.start_time = pygame.time.get_ticks() - self.elapsed_time
            self.running = True

    def stop(self):
        """Stop the timer and reset the elapsed time."""
        self.running = False
        self.elapsed_time = 0

    def pause(self):
        """Pause the timer."""
        if self.running:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.running = False

    def update(self):
        """
        Update the timer. Should be called every frame in the game loop.
        Executes the callback if the timer completes.
        """
        if self.running:
            current_time = pygame.time.get_ticks()
            if (current_time - self.start_time) / 1000 >= self.seconds:
                self.callback()
                if self.loop:
                    self.start_time = current_time
                else:
                    self.stop()