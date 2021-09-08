# MACROPAD Hotkeys example: Minecraft Effects (Creative) for Bedrock Edition

# Note: Must enable "full keyboad gameplay" to equip armor automatically.
#       This is found under "settings", then "keyboard and mouse".

# NOTE: There is a line length limit (? ~100 char ?). Exceeding that limit appears
#       to result in silent failure.  Therefore, the key sequences are split
#       across multiple lines.

from macro_actions import K, L

# See https://minecraft.fandom.com/wiki/Effect

# Unfortunately, bedrock edition has no single command that both
# gives an item and enchants it.  Thus, have to place the item in
# the player's inventory slot, enchant it, then equip it.
#
# As a result, it is probably better to learn on less complex
# macro files before attempting to adjust settings in this one.

DELAY_AFTER_COMMAND = 0.75
DELAY_AFTER_SLASH  = 0.80 # required so minecraft has time to bring up command screen
DELAY_BEFORE_RETURN = 0.10 # give minecraft time to show all the keys pressed...


# If  "full-keyboard gameplay" is not enabled, armor can be left in inventory
# CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM = Keycode.PAGE_UP
CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM = K("E")

app = {
    'name': 'Minecraft PE (equip)',
    'macros': [
        (0x003000, 'helm', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_helmet"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s protection 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s respiration 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s aqua_affinity 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM]),
        (0x003000, 'elytra', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_chestplate"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM]),
        (0x003000, 'legs', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_leggings"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s protection 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM]),
        (0x003000, 'boots', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_boots"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s protection 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s feather_falling 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s depth_strider 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s soul_speed 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM]),
        (0x003000, 'frosty', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_boots"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s protection 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s feather_falling 4"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s frost_walker 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s soul_speed 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            CONFIGURABLE_KEY_EQUIP_CURRENTLY_HELD_ITEM]),
        (0x300000, 'feedme', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_sword"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s fire_aspect 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s knockback 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s looting 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s sharpness 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x300000, 'excal', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_sword"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s fire_aspect 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s knockback 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s looting 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s sharpness 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x300000, 'trident', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy trident"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s loyalty 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s channeling 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s riptide 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s impaling 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x300000, 'bow', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy bow"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s power 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s punch 2"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x000030, 'silky', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_pickaxe"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s efficiency 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s silk_touch 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x000030, 'pickme', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_pickaxe"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s efficiency 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s fortune 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
        (0x000030, 'axe', [
            L("/"), DELAY_AFTER_SLASH,
            L("replaceitem entity @s slot.weapon.mainhand 0 destroy netherite_axe"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s mending 1"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s fortune 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s efficiency 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s sharpness 5"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            L("/"), DELAY_AFTER_SLASH,
            L("enchant @s unbreaking 3"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN"), DELAY_AFTER_COMMAND,
            K("PAGE_UP"), -K("PAGE_UP")]),
    ]
}