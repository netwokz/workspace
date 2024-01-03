import random
import uuid

# uuid_format = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx"
uuid_format_regex = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
# uuid_length = 32
uuid_varient = "89ab"


def generate_uuid(count):
    for i in range(count):
        new_uuid = uuid.uuid4()
        print(f"{i}: {new_uuid}")


def generate_my_uuid(count=1):
    chars = "0123456789abcdef"
    for x in range(count):
        uuid_chars_1 = random.choices(chars, k=8)
        v1 = "".join(uuid_chars_1)

        uuid_chars_2 = random.choices(chars, k=4)
        v2 = "".join(uuid_chars_2)

        uuid_chars_3 = random.choices(chars, k=3)
        v3 = "".join(uuid_chars_3)

        uuid_chars_4 = random.choices(chars, k=3)
        varient = random.choice(uuid_varient)
        v4 = "".join(uuid_chars_4)

        uuid_chars_5 = random.choices(chars, k=12)
        v5 = "".join(uuid_chars_5)
        print(f"{v1}-{v2}-{4}{v3}-{varient}{v4}-{v5}")


# generate_uuid(6)
generate_my_uuid(60)
