class User:
    def __init__(self, gender, age, weight, height, activity, diet_type, lifestyle, target):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.diet_type = [r.casefold() for r in diet_type]
        self.lifestyle = lifestyle
        self.target = target

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, g):
        valid_gender = ["f", "m"]
        if not isinstance(g, str) or g.casefold() not in valid_gender:
            raise ValueError("Invalid gender")
        self._gender = g.casefold()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, a):
        if not isinstance(a, int) or a <= 0 or a > 120:
            raise ValueError("Invalid age")
        self._age = a

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        if w <= 0 or w > 600:
            raise ValueError("Invalid weight")
        self._weight = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        if h <= 50 or h > 300:
            raise ValueError("Invalid height")
        self._height = h

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        valid_target = ["lose", "gain", "maintain"]
        if not isinstance(t, str) or t.casefold() not in valid_target:
            raise ValueError("Invalid target")
        self._target = t.casefold()
