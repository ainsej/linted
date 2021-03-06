import os
import json
import collections

from django.conf import settings


def tree(mapping=[]):
    return collections.defaultdict(tree, mapping)


class ScannerSettings():
    def __init__(self, repository_scanner):
        scanner_name = repository_scanner.scanner.short_name
        scanner_language = repository_scanner.scanner.language.short_name

        ruleset_file = os.path.join(settings.SCANNER_DIR, scanner_language, scanner_name, 'ruleset.json')
        with open(ruleset_file) as f:
            self.ruleset = json.loads(f.read())

        if repository_scanner.settings == '':
            self.settings = tree()
        else:
            self.settings = json.loads(repository_scanner.settings, object_pairs_hook=tree)

        self.repository_scanner = repository_scanner

    def clear_settings(self):
        self.settings = tree()

    def set_scanner_config(self, config):
        self.settings['config'] = config

    def get_scanner_config(self):
        return self.settings['config']

    def get_scanner_rules(self):
        return self.settings['rules']

    def get_custom_rule_properties(self, ruleset, rule):
        return self.settings['rules'][ruleset][rule]['properties']

    def get_property_value(self, ruleset, rule, property):
        custom_property_value = self.get_custom_property_value(ruleset, rule, property)
        if custom_property_value is not None:
            return custom_property_value
        else:
            (default_type, default_value) = self.get_default_property(ruleset, rule, property)
            return default_value

    def get_rule_enabled(self, ruleset, rule):
        custom_enabled_value = self.settings['rules'][ruleset][rule].get('enabled')
        if custom_enabled_value is not None:
            return custom_enabled_value
        else:
            default_enabled_value = self.ruleset[ruleset]['rules'][rule]['enabled']
            return default_enabled_value

    def set_rule_enabled(self, ruleset, rule, enabled):
        default_enabled_value = self.ruleset[ruleset]['rules'][rule]['enabled']
        if default_enabled_value != enabled:
            self.settings['rules'][ruleset][rule]['enabled'] = enabled

    def get_default_property(self, ruleset, rule, property):
        try:
            ruleset_property = self.ruleset[ruleset]['rules'][rule]['properties'][property]
            property_type = ruleset_property['type']
            default_value = ruleset_property['default']

            return property_type, default_value
        except KeyError:
            return None

    def get_custom_property_value(self, ruleset, rule, property):
        custom_rule_properties = self.get_custom_rule_properties(ruleset, rule)
        return custom_rule_properties.get(property)

    def add_custom_rule(self, ruleset, rule, property, value):
        default_rule = self.get_default_property(ruleset, rule, property)
        if default_rule is not None:
            property_type, default_value = default_rule

            #Change type if property is a boolean
            if property_type == 'bool':
                value = (value == 'true')

            if value != default_value:
                properties = self.get_custom_rule_properties(ruleset, rule)
                properties[property] = value

    def save(self):
        self.repository_scanner.settings = json.dumps(self.settings)
        self.repository_scanner.save()
