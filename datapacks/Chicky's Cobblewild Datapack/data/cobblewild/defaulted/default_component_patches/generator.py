import json
from pathlib import Path

NAMESPACE = "cobblewild"

ADD = "add_value"
MULT = "add_multiplied_base"

class AttributeHandler():
    def __init__(self, id: str, mods: tuple):
        self.id = id
        self.mods = mods
            
    def buildModifier(self, level: int, attr: str, operation: str):
        return {
            "type": attr,
            "id": f"{NAMESPACE}:{attr.split(":")[1]}",
            "amount": level,
            "operation": operation,
            "slot": "mainhand"
        }
        
    def getPatch(self, level: int):
        modifiers = []
        
        for attr, amounts in self.mods.items():
            index = amounts[1][level - 1]
            if index:
                modifiers.append(self.buildModifier(index, attr, amounts[0]))
            
        return modifiers
        
FIRE = AttributeHandler("fire", {
    "spell_power:fire": (ADD, [3, 5, 6.5, 8]),
    "spell_power:critical_damage": (MULT, [0, 0, 0.03, 0.06])
})
ARCANE = AttributeHandler("arcane", {
    "spell_power:arcane": (ADD, [3, 5, 6.5, 8])
})
FROST = AttributeHandler("frost", {
    "spell_power:frost": (ADD, [3, 5, 6.5, 8])
})
AIR = AttributeHandler("air", {
    "spell_power:air": (ADD, [3, 5, 6.5, 8])
})
EARTH = AttributeHandler("earth", {
    "spell_power:earth": (ADD, [3, 5, 6.5, 8]),
    "spell_power:critical_chance": (MULT, [0, 0, 0.05, 0.15])
})
WATER = AttributeHandler("water",  {
    "spell_power:water": (ADD, [3, 5, 6.5, 8]),
    "spell_power:haste": (MULT, [0, 0, 0.03, 0.05])
})
HEALING = AttributeHandler("support",  {
    "spell_power:healing": (ADD, [3, 5, 6.5, 8])
})
BOW = AttributeHandler("bow",  {
    "ranged_weapon:pull_time": (ADD, [8, 9.5, -0.1, -0.5]),
    "ranged_weapon:velocity": (ADD, [1.5, 1.5, 1.5, 1.5]),
    "ranged_weapon:damage": (ADD, [8, 9.5, 11, 13.5])
})
ROGUE = AttributeHandler("rogue", {
    "spell_engine:evasion_chance": (MULT, [0, 0.025, 0.05, 0.075])
})
FIST = AttributeHandler("fist", {
    "mrpg_lib:arcane_fuse_modifier": (MULT, [0.025, 0.05, 0.075, 0.075]),
    "minecraft:generic.attack_speed": (MULT, [0, 0, 0.01, 0.025])
})
WARRIOR = AttributeHandler("warrior", {
    "minecraft:generic.attack_speed": (MULT, [0, 0, 0.01, 0.025]),
    "critical_strike:chance": (MULT, [0, 0, 0.05, 0.15])
})
BERSERKER = AttributeHandler("berserker", {
    "mrpg_lib:rage_modifier": (MULT, [0.025, 0.025, 0.05, 0.075]),
    "critical_strike:damage": (MULT, [0, 0, 0.03, 0.06])
})

attributes = [FIRE, ARCANE, FROST, AIR, EARTH, WATER, HEALING, BOW, ROGUE, FIST, WARRIOR, BERSERKER]

with open("weapons.json", "r") as f:
    weapons = f.read()
    weapons = json.loads(weapons)
    
    for item, modifiers in weapons.items():
        patch = {
            "elements": [
                item
            ],
            "patch_generators": [
                {
                    "generator": "defaulted:modify_attribute_modifiers",
                    "to_add": {
                        "modifiers": []
                    },
                    "to_remove": []
                }
            ]
        }
        
        for id, level in modifiers.items():
            for attr in attributes:
                if id == attr.id:
                    patch["patch_generators"][0]["to_add"]["modifiers"].extend(attr.getPatch(int(level)))
              
        item_name = item.split(":")      
        with open(f"{item_name[0].strip("#")}_{item_name[1]}.json", "w") as patches:
            patches.write(json.dumps(patch, indent = 2))