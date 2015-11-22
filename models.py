class Page:
    def __init__(self, id, text, image=None):
        self.id = id
        self.text = text

        if image:
            self.image = '/static/images/{0}'.format(image)
        else:
            self.image = None

    def to_json(self):
        if self.image:
            return {
                'id': self.id,
                'image': self.image,
                'text': self.text,
            }
        else:
            return {
                'id': self.id,
                'text': self.text,
            }


class Question(Page):
    def __init__(self, id, text, result_yes, result_no, image=None):
        super().__init__(id, text, image)
        self.result_yes = result_yes
        self.result_no = result_no


class Statement(Page):
    def __init__(self, id, text, image=None):
        super().__init__(id, text, image)
