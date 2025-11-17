from uuid import uuid4


class Event:
    def __init__(self, object_id, user_id, description, timestamp, id=None):
        self.id = id or uuid4()
        self.object_id = object_id
        self.user_id = user_id
        self.description = description
        self.timestamp = timestamp

    def update_description(self, new_desc):
        if len(new_desc) < 3:
            raise ValueError("Description too short")
        self.description = new_desc
