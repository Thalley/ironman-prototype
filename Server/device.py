#Internal device class
class Device(object):    
    def __init__(self, id, name, coords, actions, url, state = 'off'):
        self.id = id
        self.name = name
        self.coords = coords
        self.actions = actions
        self.state = state
        self.url = url

    def canPerformAction(self, action):
      return action in self.actions

    # Makes the object serializable
    def serialize(self):
      return {
        'id': self.id,
        'name': self.name,
        'coords': self.coords,
        'actions': self.actions,
        'state': self.state,
        'url': self.url,
      }