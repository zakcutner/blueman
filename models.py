class Page:
    def __init__(self, id, image, text):
        self.id = id
        self.image = '/static/images/{0}'.format(image)
        self.text = text

    def to_json(self):
        return {
            'id': self.id,
            'image': self.image,
            'text': self.text,
        }


class Question(Page):
    def __init__(self, id, image, text, result_yes, result_no):
        super().__init__(id, image, text)
        self.result_yes = result_yes
        self.result_no = result_no


class Statement(Page):
    def __init__(self, id, image, text):
        super().__init__(id, image, text)
