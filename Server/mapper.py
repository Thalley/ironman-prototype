#Maps actions between server and HomePort

#The mappings as tuples
MAPPINGS = [('0', 'turnOff'), ('1', 'turnOn')]

#Maps from HomePort ID to action
def map_id_to_action(id):
    mapping = [tup for tup in MAPPINGS if tup[0] == id]
    if mapping:
        return mapping[0][0]
    else:
        raise LookupError("The action ID \"" + id + "\" could not be found in the mappings")

#Maps from action to HomePort ID
def map_action_to_id(action):
    mapping = [tup for tup in MAPPINGS if tup[1] == action]
    if mapping:
        return mapping[0][0]
    else:
        raise LookupError("The action \"" + action + "\" could not be found in the mappings")