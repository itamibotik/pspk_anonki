message_queues = {}

def add_message_to_queue(user_id, message):
    if user_id not in message_queues:
        message_queues[user_id] = []
    message_queues[user_id].append(message)

def get_next_message(user_id):
    if user_id in message_queues and message_queues[user_id]:
        return message_queues[user_id].pop(0)
    return None

def has_pending_messages(user_id):
    return user_id in message_queues and bool(message_queues[user_id])
