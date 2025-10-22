import math

# Write a class called Rectangle, with attributes with and height,
# and methods to calculate the area and perimeter. The class should
# also have a __str__ method that returns a string representation
# in a form you can infer from the unit tests below.


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return self.width * 2 + self.height * 2

    def __str__(self):
        return f"Rectangle({self.width} x {self.height})"

# Write a class called Circle, with an attribute radius,
# and methods to calculate the area and circumference.
# Implement the __str__ method according to the unit tests
# below.

# ...


# Write a class called Song, with attributes title, artist, and
# duration. The duration should be in seconds. The class should
# have a __str__ method that returns a string representation
# according the unit tests below, and a method called play that
# prints a message inferrable from the unit tests below.

# ...


# Write a class called Playlist, which contains a list of Song
# objects. The class should have methods to add a song, play all
# songs, and a __str__ method that returns a string representation
# of the playlist, with each song represented as "title by artist
# (duration)s" and separated by a pipe character (|). If the playlist
# is empty, the __str__ method should return "Playlist is empty."

# ...

# Keep the following tests in your file. Use them as you do the work
# in this assignment. (And remember to remove this comment before
# submission.)


def test_rectangle():
    rect = Rectangle(3, 4)
    assert rect.area() == 12
    assert rect.perimeter() == 14
    assert str(rect) == "Rectangle(3 x 4)"


def test_circle():
    circle = Circle(5)
    assert circle.area() == 25*math.pi
    assert circle.circumference() == 10*math.pi
    assert str(circle) == "Circle(radius=5)"


def test_song(capfd):
    song = Song("Night Shift", "Lucy Dacus", 391)
    assert str(song) == "Night Shift by Lucy Dacus (391s)"
    song.play()
    captured_output = capfd.readouterr()
    assert captured_output.out == (
        "Playing Night Shift by Lucy Dacus (391s)\n"
    )


def test_playlist(capfd):
    playlist = Playlist()
    song1 = Song("Night Shift", "Lucy Dacus", 391)
    song2 = Song("I Was Neon", "Julia Jacklin", 243)
    song3 = Song("Forgiveness", "Alice Glass", 191)
    playlist.add_song(song1)
    playlist.add_song(song2)
    playlist.add_song(song3)
    assert str(playlist) == (
        "Night Shift by Lucy Dacus (391s)|"
        "I Was Neon by Julia Jacklin (243s)|"
        "Forgiveness by Alice Glass (191s)"
    )
    playlist.play_all()
    captured_output = capfd.readouterr()
    assert captured_output.out == (
        "Playing Night Shift by Lucy Dacus (391s)\n"
        "Playing I Was Neon by Julia Jacklin (243s)\n"
        "Playing Forgiveness by Alice Glass (191s)\n"
    )
