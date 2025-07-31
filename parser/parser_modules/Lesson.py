class Lesson(object):
    def __init__(
        self,
        name='',
        teacher_name='',
        location='',
        group='',
        start="01-01-1970T00:00",
        end="01-01-1970T00:00",
        link=''
    ):
        self.id = 0
        self.name = name
        self.teacher = teacher_name
        self.location = location
        self.group = group
        self.start = start
        self.end = end
        self.link = link
        
    def from_tuple(self, tuple):
        self.id = tuple[0]
        self.name = tuple[1]
        self.teacher = tuple[2]
        self.location = tuple[3]
        self.group = tuple[4]
        self.start = tuple[5]
        self.end = tuple[6]
        self.link = tuple[7]
        return self 

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return (
                self.name == other.name
                and self.teacher == other.teacher
                and self.location == other.location
                and self.group == other.group
                and self.start == other.start
                and self.end == other.end
                and self.link == other.link
            )
        return False

    def add_date(self, start, end):
        self.start = start
        self.end = end

    def get_tuple(self):
        return self.name, self.teacher, self.location, self.group, self.start, self.end, self.link
    
    def copy(self):
        return Lesson(self.name, self.teacher, self. location, self.group, self.start, self.end, self.link)
