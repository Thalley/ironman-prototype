#Maps actions between server and HomePort

#The mappings as tuples
MAPPINGS = [('0', 'off'), ('1', 'on')]

#Maps from HomePort ID to action
def map_id_to_action(id):
    mapping = [tup for tup in MAPPINGS if tup[1] == action]
    if mapping:
        return mapping[0][0]
    else:
        return None

#Maps from action to HomePort ID
def map_action_to_id(action):
    mapping = [tup for tup in MAPPINGS if tup[1] == action]
    if mapping:
        return mapping[0][0]
    else:
        return None