import csv
import os
import random
import secrets


def get_device():
    file = open("csv_files/devices.csv")
    devices = csv.reader(file)
    device = random.choice(list(devices))
    file.close()
    return device[2] + " " + device[0]


def get_uniqueid():
    return secrets.token_hex(16)


def get_os():
    return "Android OS %s.%s.%s / API- %s (QP%sA.%s.020/%s%s)" % (
        random.randint(7, 11),
        random.randint(1, 9),
        random.randint(1, 9),
        random.randint(15, 30),
        random.randint(1, 9),
        random.randint(100000, 999999),
        random.randint(10000, 99999),
        random.randint(1000, 9999)
    )


def get_gpu():
    file = open("csv_files/gpus.csv")
    gpus = csv.reader(file)
    gpu = random.choice(list(gpus))
    file.close()
    return gpu[0]


def get_cpu():
    file = open("csv_files/cpus.csv")
    cpus = csv.reader(file)
    cpu = random.choice(list(cpus))
    file.close()
    if cpu is not None:
        if type(cpu) == str:
            return cpu
        elif type(cpu) == list:
            return cpu[0]
    else:
        return "Snapdragon 888"


def generate_username(num_results=1):
    directory_path = os.path.dirname(__file__)
    adjectives, nouns = [], []
    with open(os.path.join(directory_path, 'csv_files', 'adjectives.csv'), 'r') as file_adjective:
        with open(os.path.join(directory_path, 'csv_files', 'nouns.csv'), 'r') as file_noun:
            for line in file_adjective:
                adjectives.append(line.strip())
            for line in file_noun:
                nouns.append(line.strip())

    usernames = []
    for _ in range(num_results):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns).capitalize()
        num = str(random.randrange(100))
        x = random.randint(1, 10)
        if x == 4:
            usernames.append(adjective + noun + num)
        usernames.append(adjective + noun)
    return usernames
