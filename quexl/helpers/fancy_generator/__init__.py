from quexl.helpers.fancy_generator.push_id import PushID


def fancy_id_generator():
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    return push_id.next_id()


# # associate the listener function with models, to execute during the
# # "before_insert" event
# tables = [
#     User, Address
# ]
#
# for table in tables:
#     event.listen(table, 'before_insert', fancy_id_generator)
