'''
Generates ui-lovelace.yaml based on entities in configuration.yaml, with optional arguments

Replaces an existing ui-lovelace.yaml, so make sure to back up your old version


usage: change_ui_cards.py [-h] [-a [ADD [ADD ...]]] [-c] [-d [DELETE [DELETE ...]]]

optional arguments:
  -h, --help            show help message and exit
  -a [ADD [ADD ...]], --add [ADD [ADD ...]]
                        Add given space-separated entities as a card to ui-lovelace.yaml, the first argument will be the column
                        to add the card to, 1 being middle column and 2 being right column.
                        Empty will add all defined entities
  -c, --configuration   Process configuration.yaml to update list of entities to draw from (must be included during
                        first run)
  -d [DELETE [DELETE ...]], --delete [DELETE [DELETE ...]]
                        Delete card with given space-separated entities from ui-lovelace.yaml, first argument lets you delete
                        a specific card or column (0 to delete specific card, 1 to delete all cards in middle column, 
                        2 to delete all cards in right column, empty (no arguments) will delete all entities.
                        Note that an empty argument for --add will supercede this command.

'''
import argparse
import os
import yaml


# Custom card's design
CUSTOM_CARD = {'cards': [
    {'type': 'entities', 'entities': [
        {'entity': 'input_select.order'}
    ]},
    {'type': 'entities', 'entities': [
        {'entity': 'input_select.flavor'}
    ]},
    {'type': 'entities', 'entities': [
        {'entity': 'input_text.token'}
    ]},
    {'type': 'button', 'entity': 'input_boolean.add_event', 'show_icon': False},
    {'type': 'button', 'entity': 'input_boolean.run_helion', 'show_icon': False},
    {'type': 'button', 'entity': 'input_boolean.next_event', 'show_icon': False},
    {'type': 'button', 'entity': 'input_boolean.reset', 'show_icon': False}
], 'title': 'Settings', 'type': 'vertical-stack'}

# Name of ui file (ui-lovelace.yaml default)
UI_FILE = 'helion.yaml'


class Loader(yaml.SafeLoader):
    # Loader class for '!include' in configuration.yaml
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node) -> list:
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


def parse_ui_lovelace() -> list:
    '''
    Parses entities on the current ui-lovelace.yaml and returns a list of entities.
    '''
    ui_load = None
    try:
        with open(UI_FILE, 'r') as stream:
            ui_load = yaml.load(stream, Loader)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'No {UI_FILE} to parse.') from e
    except yaml.YAMLError as exc:
        print(exc)

    if not ui_load:
        return []

    current_entities = []
    if 'views' in ui_load:
        # List of all cards on ui
        cards = ui_load['views'][0]['cards'][0]['cards']

        # Input cards column (middle column)
        for input_card in cards[1]['cards']:
            entities_in_card = []

            # Targets the device cards
            if 'entities' in input_card and 'type' in input_card and input_card['type'] == 'glance':

                # entity_group contains entity id, along with tags that prevent clicking
                for entity_group in input_card['entities']:
                    entity = entity_group['entity'] if 'entity' in entity_group else None
                    if entity:
                        entities_in_card.append(entity)
                # Second value in tuple referring to column
                current_entities.append((entities_in_card, 1))

        # Input cards column (right column)
        for input_card in cards[2]['cards']:
            entities_in_card = []

            # Targets the device cards
            if 'entities' in input_card and 'type' in input_card and input_card['type'] == 'glance':

                # entity_group contains entity id, along with tags that prevent clicking
                for entity_group in input_card['entities']:
                    entity = entity_group['entity'] if 'entity' in entity_group else None
                    if entity:
                        entities_in_card.append(entity)
                current_entities.append((entities_in_card, 2))

    return current_entities


def config_parse_all() -> list:
    '''
    Parses entire configuration.yaml, and creates or replaces the entities.txt list of entities, returning the new list.
    '''
    config_load = None
    try:
        with open('configuration.yaml', 'r') as stream:
            config_load = yaml.load(stream, Loader)
    except FileNotFoundError as e:
        raise FileNotFoundError('No configuration.yaml to process.') from e
    except yaml.YAMLError as exc:
        print(exc)

    if not config_load:
        return []

    ui_output_tags = []
    for item in config_load:
        parent_tag = config_load[item]  # List of items under each tag
        if item and item == 'input_select':  # Input_select tags
            for input_select in parent_tag:
                current_name = parent_tag[input_select]['name']
                if current_name:
                    current_name = current_name.split(',')[0]
                select_name = current_name if current_name else input_select
                ui_output_tags.append(
                    ('input_select.' + input_select, select_name))

        elif parent_tag and isinstance(parent_tag, list):  # Other tags
            first_tag = parent_tag[0]

            # Template tags (switches etc)
            if first_tag and isinstance(first_tag, dict) and 'platform' in first_tag:
                if first_tag['platform'] == 'template' and len(first_tag) == 2:

                    # Getting the entities
                    for tag in first_tag:
                        if tag != 'platform':
                            for entity_tag in first_tag[tag]:
                                # Adds entity and its name
                                entity = first_tag[tag][entity_tag]
                                entity_name = entity['friendly_name'] if 'friendly_name' in entity else entity_tag
                                ui_output_tags.append(
                                    (item + '.' + entity_tag, entity_name))  # Entity's id is its entity type + . + the entity tag
    if ui_output_tags:
        with open('entities.txt', 'w') as entities_file:
            for tag in ui_output_tags:
                entities_file.write(tag[0] + ',' + tag[1] + '\n')
        print('Generated new entities.txt')

    return ui_output_tags


def parse_existing() -> list:
    '''
    Parses existing entities.txt and returns the list of entities.
    '''
    ui_output_tags = []
    try:
        with open('entities.txt', 'r') as entities:
            for entity in entities:
                split_entity = entity.rstrip().split(',')
                ui_output_tags.append((split_entity[0], split_entity[1]))
    except FileNotFoundError as e:
        raise FileNotFoundError(
            'No entities.txt! Please parse the configuration.yaml first with the -c argument.') from e

    return ui_output_tags


def modify_ui(tags_list: list, compare_list: list = None) -> None:
    '''
    Modifies the ui-lovelace.yaml cards to be the given list of entities. Optionally sorts list and compares to a different list.
    '''
    if tags_list or tags_list == []:
        # Create the cards on ui-lovelace.yaml
        input_cards = []
        output_cards = []

        for output_tag in tags_list:
            # Grouping multiple entities
            card_group = []
            for entity in output_tag[0]:
                card_group.append({'entity': entity,
                                   'tap_action': {'action': 'none'},
                                   'hold_action': {'action': 'none'}})
            # Specifying column to add to
            if output_tag[1] == 1:
                input_cards.append({'type': 'glance', 'entities': card_group})
            elif output_tag[1] == 2:
                output_cards.append({'type': 'glance', 'entities': card_group})

        ui_lovelace_yaml = {'title': 'Helion', 'views': [
            {'path': 'helion',
             'title': 'Helion',
             'icon': 'mdi:home-variant',
             'panel': True,
             'cards': [{
                 'type': 'grid',
                 'gridrows': 'auto auto auto',
                 'gridcols': '30% 30% 30%',
                 'columns': 3,
                 'square': False,
                 'cards': [CUSTOM_CARD,
                           {'type': 'vertical-stack',
                               'title': 'Input', 'cards': input_cards},
                           {'type': 'vertical-stack',
                               'title': 'Output', 'cards': output_cards}
                           ]
             }]
             }]}

        # Replaces existing ui-lovelace.yaml
        with open(UI_FILE, 'w') as f:
            f.write(yaml.dump(ui_lovelace_yaml))

        if compare_list and tags_list == compare_list:
            print(f'No update to {UI_FILE}')
        else:
            print(f'Updated {UI_FILE}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create cards on the Home Assistant Lovelace dashboard.')
    parser.add_argument(
        '-a', '--add',
        help=f'Add given space-separated entities as a card to {UI_FILE}, and the first argument has to be the column number (1 for middle column, 2 for right column), empty will add all defined entities',
        nargs='*')
    parser.add_argument(
        '-c', '--configuration',
        help='Process configuration.yaml to update list of entities to draw from (must be included during first run)',
        action='store_true')
    parser.add_argument(
        '-d', '--delete',
        help=f'Delete card representing given space-separated entities from {UI_FILE}, first argument lets you delete a specific card or column (0 to delete specific card, 1 to delete all cards in middle column, 2 to delete all cards in right column. No arguments will delete all entities. Note that an empty argument for --add  will supercede this command.',
        nargs='*')

    args = parser.parse_args()

    Loader.add_constructor('!include', Loader.include)

    print('Entities to add:', args.add if args.add != [] else 'All')

    print('Entities to delete:', args.delete if args.delete != [] else 'All')

    entities = config_parse_all() if args.configuration else parse_existing()
    original_cards = parse_ui_lovelace()
    current_cards = original_cards.copy()

    if args.delete:  # Delete given entities
        column_to_delete = args.delete[0]
        # 0: delete specific
        if not column_to_delete.isnumeric() or int(column_to_delete) not in [0, 1, 2]:
            print(f'{column_to_delete} is not a valid column number')
        else:
            if args.delete[0] == "0":  # Delete specific card
                card_to_delete = []
                for delete_entity in args.delete[1:]:
                    card_to_delete.append(delete_entity)

                found = False
                for entity in list(current_cards):
                    if entity[0] == card_to_delete:
                        current_cards.remove(entity)
                        found = True
                        break
                if not found:
                    print(
                        f'No card deleted because {delete_entity} was not on the dashboard'
                    )
            elif args.delete[0] == "1" or args.delete[0] == "2":  # Delete entire column
                delete_col = int(args.delete[0])
                for entity in list(current_cards):
                    if entity[1] == delete_col:
                        current_cards.remove(entity)
                print(f'Deleting column {args.delete[0]}')

    elif not args.delete and args.delete != None:  # Clear list of entities
        current_cards = []

    if args.add:
        column_to_add_to = args.add[0]
        if not column_to_add_to.isnumeric() or int(column_to_add_to) not in [1, 2]:
            print(f'{column_to_add_to} is not a valid column number')
        else:
            insert_cards = []
            for add_entity in args.add[1:]:
                found = False
                for entity in entities:
                    if entity[0] == add_entity:
                        insert_cards.append(entity[0])
                        found = True
                        break
                if not found:
                    print(
                        add_entity, 'was not added because it was not in defined entities')
            if insert_cards:
                current_cards.append((insert_cards, int(column_to_add_to)))
            modify_ui(current_cards, compare_list=original_cards)
    elif not args.add and args.add != None:  # Adds all entities
        current_cards = []
        entities.sort(key=lambda x: x[1])
        for entity in entities:
            current_cards.append(([entity[0]], 1))
        modify_ui(current_cards)

    # Otherwise just check if cards were modified at all (deletion)
    elif args.add == None:
        modify_ui(current_cards, compare_list=original_cards)
