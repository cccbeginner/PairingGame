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
        self.elapsed_time = 0
        self.running = True

    def update(self, delta):
        """
        Update the timer. Should be called every frame in the game loop.
        Executes the callback if the timer completes.
        """
        if self.running:
            self.elapsed_time += delta
            if self.elapsed_time >= self.seconds:
                self.callback()
                if self.loop:
                    self.elapsed_time = 0
                else:
                    self.running = False