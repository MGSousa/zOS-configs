# -*- coding: utf-8 -*-
import os
import socket
import subprocess
import distro
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401
import sys


# Config imports
def reload(module):
    if module in sys.modules:
        importlib.reload(sys.modules[module])


mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"
myBrowser = "firefox"

"""
NOT USED AT ALL
if "arch" in distro.like():
    myDistro = "Arch"
    updateCmd = "-e sudo pacman -Syu"
elif "debian" in distro.like():
    myDistro = "Debian"
    updateCmd = "-e sudo apt upgrade -y"
elif "ubuntu" in distro.like():
    myDistro = "Ubuntu"
    updateCmd = "-e sudo apt upgrade -y"
else:
    myDistro = "Fedora"
    updateCmd = "-e sudo yum update"
"""

keys = [
    ### The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launches My Terminal"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Firefox"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle through layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill active window"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    ### Switch focus to a specific monitor (out of three)
    Key([mod], "w", lazy.to_screen(0), desc="Keyboard focus to monitor 1"),
    Key([mod], "e", lazy.to_screen(1), desc="Keyboard focus to monitor 2"),
    Key([mod], "r", lazy.to_screen(2), desc="Keyboard focus to monitor 3"),
    ### Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    ### Treetab controls
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.move_left(),
        desc="Move up a section in treetab",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.move_right(),
        desc="Move down a section in treetab",
    ),
    ### Window controls
    Key([mod], "j", lazy.layout.down(), desc="Move focus down in current stack pane"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc="Move windows down in current stack",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc="Move windows up in current stack",
    ),
    Key(
        [mod],
        "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink window (MonadTall), decrease number in master pane (Tile)",
    ),
    Key(
        [mod],
        "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc="Expand window (MonadTall), increase number in master pane (Tile)",
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="normalize window size ratios"),
    Key(
        [mod],
        "m",
        lazy.layout.maximize(),
        desc="toggle window between minimum and maximum sizes",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    ### Stack controls
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch which side main pane occupies (XmonadTall)",
    ),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack",
    ),
    Key(
        [mod, "shift"],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    ### Media controls
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.widget["volume"].increase_vol(),
        desc="Raise volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.widget["volume"].decrease_vol(),
        desc="Down volume",
    ),
    Key([], "XF86AudioMute", lazy.widget["volume"].mute(), desc="Mute volume"),
    #Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute alsa_output.pci-0000_00_1f.3.analog-stereo toggle"), desc="Mute volume"),
    Key([], "XF86AudioMicMute", lazy.spawn("toggle_mute"), desc="Toggle microphone"),
    ### Screen controls
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn(os.path.expanduser("~/.config/qtile/backlight.sh inc 1")),
        desc="Increase screen backlight",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn(os.path.expanduser("~/.config/qtile/backlight.sh dec 1")),
        desc="Decrease screen backlight",
    ),
    ### Dmenu scripts && other misc tools
    ### launched using the key-chord SUPER+p followed by 'key'
    KeyChord(
        [mod],
        "p",
        [
            Key([], "h", lazy.spawn("dm-hub"), desc="List all dmscripts"),
            Key(
                [], "e", lazy.spawn("dm-confedit"), desc="Choose a config file to edit"
            ),
            Key([], "i", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
            Key([], "m", lazy.spawn("dm-man"), desc="View manpages"),
            Key([], "n", lazy.spawn("dm-note"), desc="Store and copy notes"),
            Key([], "f", lazy.spawn("dmenu_run"), desc="Search for anything"),
            Key([], "q", lazy.spawn("dm-logout"), desc="Logout menu"),
            Key([], "s", lazy.spawn("dm-secret"), desc="Scrypt credentials"),
            Key([], "x", lazy.spawn("dm-sink-switcher"), desc="Switch sink audio device"),
        ],
    ),
]

# workspace groups
groups = [
    Group("DEV", layout="ratiotile"),
    Group("WEB", layout="monadtall"),
    Group("SYS", layout="max"),
    Group("TEAMS", layout="monadtall"),
    Group("MISC", layout="monadtall"),
]
for i, group in enumerate(groups):
    keys.append(Key([mod], str(i + 1), lazy.group[group.name].toscreen()))
    keys.append(Key([mod, "shift"], str(i + 1), lazy.window.togroup(group.name)))

# layouts
layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "4682B4",
    "border_normal": "1D2330",
    "width": 100,
}
layouts = [
    # layout.MonadWide(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Stack(stacks=2, **layout_theme),
    # layout.Columns(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize=14,
        sections=["BASE"],
        section_fontsize=12,
        border_width=1,
        bg_color="1c1f24",
        active_bg="51afef",
        active_fg="000000",
        inactive_bg="888888",
        inactive_fg="1c1f24",
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=20,
        section_bottom=20,
        level_shift=10,
        vspace=3,
        panel_width=250,
    ),
]

# colors
colors = [
    ["#282c34", "#282c34"],
    ["#1c1f24", "#1c1f24"],
    ["#dfdfdf", "#dfdfdf"],
    ["#ff6c6b", "#ff6c6b"],
    ["#98be65", "#98be65"],
    ["#da8548", "#da8548"],
    ["#51afef", "#51afef"],
    ["#cccccc", "#cccccc"],
    ["#46d9ff", "#46d9ff"],
    ["#a9a1e1", "#a9a1e1"],
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(font="Ubuntu Bold", fontsize=14, padding=2, background=colors[2])
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.Image(
            filename="~/.config/qtile/logo.png",
            scale="False",
            background=colors[0],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(myTerm)},
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=9,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[6],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="block",
            block_highlight_text_color=colors[1],
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0],
        ),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.7,
        ),
        widget.CurrentLayout(foreground=colors[2], background=colors[0], padding=5),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.WindowName(foreground=colors[6], background=colors[0], padding=0),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.GenPollText(
            update_interval=5,
            func=lambda: subprocess.check_output(
                os.path.expanduser("~/.config/qtile/ps.sh")
            ).decode("utf-8"),
            font="Ubuntu Mono",
            background=colors[0],
            foreground="cccccc",
            fontsize=16,
            padding=5.0,
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.CPU(
            background=colors[0],
            format="CPU: {load_percent}%",
            fontsize=16,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(myTerm + " -e htop")},
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.Net(
            format = 'Net: {down} ↓↑ {up}',
            background = colors[0],
            padding = 0,
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e iftop')},
            fontsize = 16
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.Memory(
            foreground="#20B2AA",
            background=colors[0],
            # background = "#20B2AA",
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(myTerm + " -e htop")},
            fmt="RAM: {}",
            format="{MemUsed: .0f}{mm} ({MemPercent: .0f}%)",
            measure_mem="M",
            fontsize=16,
            padding=5,
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.DF(
            background=colors[0],
            warn_space=50,
            fontsize=16,
            format="SSD: {uf}{m} | ({r:.0f}%)",
            visible_on_warn=False,
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.BatteryIcon(
            background=colors[0],
            battery=0,
            scale=1,
            theme_path="~/.config/qtile/icons/battery_icons",
        ),
        widget.Battery(
            foreground="#FFFFFF",
            background=colors[0],
            format="{char} {percent: 2.0%}",
            notify_below=20,
            battery=0,
            fontsize=17,
            discharge_char="",
            charge_char="+",
        ),
        widget.TextBox(
            text=" ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.Volume(
            foreground=colors[1],
            background=colors[4],
            fmt="&#9738; {}",
            padding=5,
            fontsize=14,
        ),
        widget.TextBox(
            text=" ",
            font="Ubuntu Mono",
            background=colors[1],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.Clock(
            foreground=colors[4],
            background=colors[0],
            fontsize=14,
            format="%B %d - %H:%M ",
        ),
        widget.TextBox(
            text="| PrtScrn",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#ff6c6b",
            padding=5,
            fontsize=14,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("flameshot gui")},
        ),
        widget.TextBox(
            text=" | ",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="#aaaaaa",
            padding=0,
            fontsize=16,
        ),
        widget.Systray(background=colors[0], padding=2),
    ]
    return widgets_list


# Slicing removes unwanted widgets (like systray) on Monitors 1,3
def init_widgets_screen1():
    widgets_screen = init_widgets_list()
    # del widgets_screen[(len(widgets_screen)-1):len(widgets_screen)]
    return widgets_screen


# Monitor 2 will display all widgets in widgets_list
def init_widgets_screen2():
    widgets_screen = init_widgets_list()
    del widgets_screen[(len(widgets_screen) - 1) : len(widgets_screen)]
    return widgets_screen


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
    ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see an X client's wm class and name.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download, and error.
        *layout.Floating.default_float_rules,
        Match(title="Confirmation"),  # tastyworks exit box
        Match(title="Qalculate!"),  # qalculate-gtk
        Match(wm_class="kdenlive"),  # kdenlive
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like Steam games 
# want to auto-minimize themselves when losing focus
auto_minimize = True


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.screens_reconfigured
def on_screens_reconfigured():
    qtile.cmd_reload_config()
