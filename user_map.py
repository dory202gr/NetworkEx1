

def create_users_map(users_file):
    try:
        with open(users_file, 'r') as file:
            users_data = file.read()
            return create_users_map_from_file(users_data)
    except FileNotFoundError:
        print(f"Error: The file {users_file} was not found.")
        exit(1)


def create_users_map_from_file(users_data):
    users_map = dict()
    users_data_list = users_data.split("\n")[:-1]
    for user in users_data_list:
        user_data = user.split()
        users_map[user_data[0]] = user_data[1]

    return users_map

