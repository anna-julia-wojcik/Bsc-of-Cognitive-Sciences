class User:
    # Assignments that trigger setters (validation methods)
    def __init__(self, gender, age, weight, height, activity, diet_type, lifestyle, target):
        self.gender = gender  # Setting gender
        self.age = age  # Setting age
        self.weight = weight  # Setting weight
        self.height = height  # Setting height
        self.activity = activity  # Setting activity level
        self.diet_type = [r.casefold() for r in diet_type]  # Creates a list of dietary restrictions
        self.lifestyle = lifestyle  # Setting lifestyle
        self.target = target  # Setting target

    @property
    def gender(self):
        return self._gender  # Getter returns the variable's value

    @gender.setter
    def gender(self, g):  # Setter checks if specific conditions are met (gender is female or male)
        valid_gender = ["f", "m"]
        if not isinstance(g, str) or g.casefold() not in valid_gender:  # If gender is not a string or one of the valid genders - error
            raise ValueError("Invalid gender")
        self._gender = g.casefold()  # If conditions are met - save to variable

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, a):  # Setter checks if specific conditions are met (age greater than 0 and less than or equal to 120)
        if not isinstance(a, int) or a <= 0 or a > 120:  # If it doesn't meet the conditions or is not an integer - error
            raise ValueError("Invalid age")
        self._age = a

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):  # Setter checks if specific conditions are met (weight greater than 0 and less than or equal to 600)
        if w <= 0 or w > 600:  # If it doesn't meet the conditions - error
            raise ValueError("Invalid weight")
        self._weight = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):  # Setter checks if specific conditions are met (height greater than 50 and less than or equal to 300)
        if h <= 50 or h > 300:  # If it doesn't meet the conditions - error
            raise ValueError("Invalid height")
        self._height = h

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        valid_target = ["lose", "gain", "maintain"]  # Setter checks if specific conditions are met (whether the target is in the list)
        if not isinstance(t, str) or t.casefold() not in valid_target:  # If the target is not a string or doesn't belong to the list - error
            raise ValueError("Invalid target")
        self._target = t.casefold()