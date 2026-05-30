import random
import time
import os
import shutil
import math
import sys
import threading
import getpass
import subprocess
from datetime import datetime

# --- CONFIG & COLORS ---
RAINBOW = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 47, 48, 49, 50, 51, 45, 39, 33, 27, 21, 57, 93, 129, 165, 201, 200, 199, 198, 197]
GOLD, WHITE, GREY, BLOOD, VOID = 220, 255, 240, 124, 232
RESET, BOLD, BLINK = "\033[0m", "\033[1m", "\033[5m"
HIDE_CURSOR, SHOW_CURSOR = "\033[?25l", "\033[?25h"

# Global state
STALKER_ACTIVE = True
CORRUPTION_LEVEL = 0
CURRENT_PLAYER_NAME = ""
ALL_PLAYERS = []

# --- ASSETS ---
SPOOKY_FACES = [
    ["      .---.      ", "     /     \\     ", "    | () () |    ", "     \\  ^  /     ", "      |||||      "],
    ["   XXXXXXXXXXX   ", "  X  0     0  X  ", "  X           X  ", "  X   XXXXX   X  ", "   XXXXXXXXXXX   "],
    ["     _______     ", "    /       \\    ", "   /  @   @  \\   ", "  |     V     |  ", "   \\  WWWWW  /   ", "    \\_______/    "],
    ["    .-------.    ", "   /   U U   \\   ", "  |    ___    |  ", "   \\  '---'  /   ", "    '-------'    "]
]

WHISPERS = [
    "1 533 Y0U.", "R0LL 4641N.", "WHY D0 Y0U P3R5157?", 
    "7H3 V01D HUN63R5.", "6. 6. 6.", "17 15 1N3V1748L3.",
    "H3 15 C0M1N6.", "D0N'7 L00K B3H1ND U.",
    "17 15 63771N6 L473.", "D0 Y0U F33L 54F3?", "Y0UR LUCK RUN5 DRY."
]

# --- UTILS ---
def get_color(code): return f"\033[38;5;{code}m"
def get_bg(code): return f"\033[48;5;{code}m"
def clear_screen(): print("\033[H\033[J", end="", flush=True)
def get_terminal_size(): return shutil.get_terminal_size((80, 24))
def move_cursor(x, y): print(f"\033[{y};{x}H", end="")
def set_title(title): sys.stdout.write(f"\033]0;{title}\007")

def play_glitch_sound(duration=2000):
    try: subprocess.Popen(f"head -c {duration} /dev/urandom | aplay -q -f cd", shell=True, stderr=subprocess.DEVNULL)
    except: pass

def get_sanity_status(level):
    if level == 0: return "STABLE"
    if level < 3: return "SHAKEN"
    if level < 6: return "HEARING VOICES"
    if level < 9: return "FRACTURED"
    return "LOST TO THE VOID"

# --- THE STALKER ---
def stalker_loop():
    global STALKER_ACTIVE, CORRUPTION_LEVEL
    while STALKER_ACTIVE:
        if CORRUPTION_LEVEL > 1 and random.random() < (0.08 * CORRUPTION_LEVEL):
            cols, rows = get_terminal_size()
            x, y = random.randint(1, max(1, cols - 25)), random.randint(1, rows)
            phrase = random.choice(WHISPERS)
            if random.random() < 0.3 and ALL_PLAYERS:
                target = random.choice(ALL_PLAYERS)
                phrase = f"H3 15 C0M1N6 F0R {target}..." if target != CURRENT_PLAYER_NAME else f"H3LL0 {target}..."
            if random.random() < 0.1: set_title(phrase)
            sys.stdout.write(f"\033[s\033[{y};{x}H{get_color(BLOOD)}{phrase}{RESET}\033[u")
            sys.stdout.flush()
        time.sleep(random.uniform(0.5, 2.0))

# --- EFFECTS ---
def effect_subliminal():
    cols, rows = get_terminal_size()
    face = random.choice(SPOOKY_FACES)
    clear_screen()
    v_pad = (rows - len(face)) // 2
    for line in face: print(get_color(BLOOD) + line.center(cols) + RESET)
    sys.stdout.flush()
    time.sleep(0.04)

def effect_static(duration=15):
    cols, rows = get_terminal_size()
    chars = " .:-=+*#%@"
    play_glitch_sound()
    for _ in range(duration):
        clear_screen()
        screen = ""
        for _ in range(rows):
            line = "".join([random.choice(chars) if random.random() > 0.05 else "6" for _ in range(cols)])
            screen += get_color(232 + random.randint(0, 23)) + line + RESET + "\n"
        print(screen, end="", flush=True)
        time.sleep(0.04)

def effect_glitch(duration=20):
    cols, rows = get_terminal_size()
    for _ in range(duration):
        offset, row = random.randint(-5, 5), random.randint(1, rows)
        move_cursor(1, row)
        print("\033[2K", end="")
        print(" " * abs(offset) + get_color(random.choice(RAINBOW)) + "█" * (cols - abs(offset)) + RESET, end="", flush=True)
        time.sleep(0.01)

def effect_melt(level):
    cols, rows = get_terminal_size()
    screen = [[" " for _ in range(cols)] for _ in range(rows)]
    for _ in range(30 + level * 10):
        clear_screen()
        for y in range(rows - 1, 0, -1):
            for x in range(cols):
                if screen[y-1][x] != " " and random.random() < 0.4:
                    screen[y][x], screen[y-1][x] = screen[y-1][x], " "
        for x in range(cols):
            if random.random() < 0.05: screen[0][x] = get_color(BLOOD) + random.choice(["▼", "6", "X"]) + RESET
        print("\n".join(["".join(line) for line in screen]), end="", flush=True)
        time.sleep(0.05)

def effect_system_breach(name, level):
    cols, rows = get_terminal_size()
    fake_logs = [f"FAULT: BIOS_SHADOW_INTEGRITY_COMPROMISED AT 0x{random.randint(0x1000, 0xFFFF):X}", "IRQ_COLLISION_IN_TEMPORAL_BUFFER", f"KRNL: MEMORY_CORRUPTION_DETECTED_IN_USER_{name.upper()}", "VOID_DAEMON: CONNECTED TO LOCAL_SOUL_SOCKET", "ACCESSING... [66.6% COMPLETE]", "ERR: REALITY_OVERFLOW", "R380071N6 UN1V3R53..."]
    play_glitch_sound()
    for _ in range(level * 5):
        clear_screen()
        for _ in range(rows):
            if random.random() < 0.2: print(get_color(160) + random.choice(fake_logs).center(cols) + RESET)
            else: print(get_color(232 + random.randint(0, 23)) + "".join([random.choice("01ABCDEF") for _ in range(cols)]) + RESET)
        time.sleep(0.1)

def effect_singularity(level):
    cols, rows = get_terminal_size()
    cx, cy = cols // 2, rows // 2
    for r in range(1, max(cols, rows)):
        clear_screen()
        for y in range(rows):
            line = ""
            for x in range(cols):
                dist = math.sqrt((x - cx)**2 + (y - cy*2)**2)
                if abs(dist - r) < 2: line += get_color(random.choice(RAINBOW)) + "6" + RESET
                elif dist < r: line += get_bg(VOID + (int(dist) % 10)) + " " + RESET
                else: line += " "
            print(line)
        time.sleep(0.02)

def effect_cursed_13(player_name):
    cols, rows = get_terminal_size()
    play_glitch_sound(10000)
    set_title("ERROR: CURSED_SUM_DETECTED")
    hijack_text = ["13 13 13 13 13 13 13 13", f"Y0U W3R3 N3V3R 5UPP053D 70 R34CH 7H15, {player_name.upper()}.", "7H3 D1C3 H4V3 N0 M34N1N6 H3R3.", "7H3 V01D 15 N07 4 64M3.", "1 4M 1N51D3 7H3 5C4N-L1N35."]
    for i in range(100):
        clear_screen()
        for _ in range(rows):
            if random.random() < 0.1: print(get_color(BLOOD) + random.choice(hijack_text).center(cols) + RESET)
            else: print(get_color(VOID + 1) + "".join([random.choice("13 ") for _ in range(cols)]) + RESET)
        time.sleep(0.05)
    clear_screen(); print("\n" * (rows // 2)); print(get_color(BLOOD) + BOLD + BLINK + "6 0 0 D 8 Y 3".center(cols) + RESET); time.sleep(2)

# --- PHYSICS & GRAPHICS ---

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.life = 1.0
        self.char = random.choice("01")

    def draw(self, cols, rows):
        if 0 <= int(self.y) < rows and 0 <= int(self.x) < cols:
            move_cursor(int(self.x), int(self.y))
            col = 232 + int(self.life * 23) if self.color == GREY else self.color
            print(get_color(col) + self.char + RESET, end="")

class Die:
    def __init__(self, x, y, vx, vy):
        self.x, self.y, self.vx, self.vy = float(x), float(y), float(vx), float(vy)
        self.val = random.randint(1, 6)
        self.w, self.h = 13, 6
        self.trail = []

    def update(self, cols, rows, force_val=None):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5: self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18 # Gravity
        if self.x <= 2 or self.x + self.w >= cols-2: 
            self.vx *= -0.75; self.x = max(2, min(cols-self.w-2, self.x))
        if self.y <= 2 or self.y + self.h >= rows-2: 
            self.vy *= -0.65; self.vx *= 0.92; self.y = max(2, min(rows-self.h-2, self.y))
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.2: self.val = force_val if force_val else random.randint(1, 6)

    def get_art(self, color_code=WHITE, glitch=False):
        faces = {1: ["           ", "     ▄     ", "           "], 2: [" ▄         ", "           ", "         ▄ "], 3: [" ▄         ", "     ▄     ", "         ▄ "], 4: [" ▄       ▄ ", "           ", " ▄       ▄ "], 5: [" ▄       ▄ ", "     ▄     ", " ▄       ▄ "], 6: [" ▄       ▄ ", " ▄       ▄ ", " ▄       ▄ "], 7: [" ▄   ▄   ▄ ", "     ▄     ", " ▄   ▄   ▄ "], 8: [" ▄   ▄   ▄ ", " ▄       ▄ ", " ▄   ▄   ▄ "], 13: ["    █ █    ", "      █    ", "    █ █    "]}
        val = self.val if self.val in faces else 6
        rs = faces[val]
        if glitch: rs = ["".join([c if random.random() > 0.15 else random.choice("6X#") for c in r]) for r in rs]
        c, s = get_color(color_code) + BOLD, get_color(VOID + 4)
        return [c + "▄▄▄▄▄▄▄▄▄▄▄▄▄" + RESET, c + "█ " + rs[0] + " █" + s + "▒" + RESET, c + "█ " + rs[1] + " █" + s + "▒" + RESET, c + "█ " + rs[2] + " █" + s + "▒" + RESET, c + "▀▀▀▀▀▀▀▀▀▀▀▀▀" + s + "▒" + RESET, " " + s + "▒▒▒▒▒▒▒▒▒▒▒▒▒" + RESET]

def draw_ui(current_player, corruption):
    cols, rows = get_terminal_size()
    sanity = get_sanity_status(corruption)
    col = BLOOD if corruption > 4 else GOLD
    move_cursor(1, 1)
    bar = f" ▚ {current_player} ▞  SANE_LEVEL: {sanity}  ▚ CORRUPTION: {corruption} ▞ "
    print(get_color(col) + "█" + bar.center(cols-2, "▀") + "█" + RESET)
    move_cursor(1, rows)
    prompt = " [ PRESS ENTER TO ROLL | 'Q' TO ABANDON ] "
    print(get_color(GREY) + "▀" * ((cols-len(prompt))//2) + prompt + "▀" * (cols - ((cols-len(prompt))//2) - len(prompt)) + RESET)

def roll_physics_dice(level, player_name):
    cols, rows = get_terminal_size()
    d1 = Die(cols*0.2, 5, random.uniform(3, 6), random.uniform(0, 2))
    d2 = Die(cols*0.7, 5, random.uniform(-6, -3), random.uniform(0, 2))
    is_cursed = (random.random() < 0.03 + (level * 0.01))
    f1, f2 = ( (6, 7) if random.random() > 0.5 else (7, 6) ) if is_cursed else (None, None)
    if is_cursed and level > 7: f1, f2 = 13, 13
    particles = []
    for _ in range(80):
        if random.random() < (level * 0.03): effect_subliminal()
        d1.update(cols, rows, force_val=f1); d2.update(cols, rows, force_val=f2)
        if random.random() < 0.5: particles.append(Particle(d1.x + 5, d1.y + 3, GREY))
        if random.random() < 0.5: particles.append(Particle(d2.x + 5, d2.y + 3, GREY))
        clear_screen(); draw_ui(player_name, level)
        for p in particles[:]:
            p.life -= 0.1
            if p.life <= 0: particles.remove(p)
            else: p.draw(cols, rows)
        art1, art2 = d1.get_art(glitch=(level>2)), d2.get_art(glitch=(level>2))
        for i, line in enumerate(art1): move_cursor(int(d1.x), int(d1.y)+i); print(line, end="")
        for i, line in enumerate(art2): move_cursor(int(d2.x), int(d2.y)+i); print(line, end="")
        sys.stdout.flush(); time.sleep(0.03)
        if abs(d1.vx) < 0.1 and abs(d1.vy) < 0.2 and abs(d2.vx) < 0.1 and abs(d2.vy) < 0.2: break
    return d1.val, d2.val

def get_players():
    players = []
    set_title("THE VOID CALLS...")
    while True:
        cols, rows = get_terminal_size()
        clear_screen(); draw_ui("INITIALIZING...", 0)
        move_cursor(1, rows // 2 - 2)
        print(get_color(GOLD) + BOLD + " 3N73R PL4Y3R N4M3 ".center(cols) + RESET)
        if players:
            move_cursor(1, rows // 2 - 1)
            print(get_color(GREY) + f" (Current players: {', '.join(players)}) ".center(cols) + RESET)
        move_cursor(1, rows // 2)
        print(get_color(GREY) + " [ Leave empty to start ] ".center(cols) + RESET)
        move_cursor(cols // 2 - 10, rows // 2 + 2)
        print(get_color(WHITE) + "> ", end="", flush=True)
        name = sys.stdin.readline().strip().upper()
        if not name:
            if not players: players.append(getpass.getuser().upper())
            break
        if name not in players: players.append(name)
    return players

def main():
    global CORRUPTION_LEVEL, STALKER_ACTIVE, CURRENT_PLAYER_NAME, ALL_PLAYERS
    print(HIDE_CURSOR)
    ALL_PLAYERS = get_players()
    player_data = {name: {"corruption": 0} for name in ALL_PLAYERS}
    initial_corruption = 5 if "--scare" in sys.argv else 0
    for name in player_data: player_data[name]["corruption"] = initial_corruption
    threading.Thread(target=stalker_loop, daemon=True).start()
    try:
        while True:
            for current_player in ALL_PLAYERS:
                CURRENT_PLAYER_NAME = current_player
                corruption = player_data[current_player]["corruption"]
                CORRUPTION_LEVEL = corruption
                cols, rows = get_terminal_size()
                sanity = get_sanity_status(corruption)
                set_title(f"{current_player} | {sanity} ({corruption})")
                clear_screen(); draw_ui(current_player, corruption)
                
                # Turn Start Prompt
                move_cursor(1, rows // 2)
                print(get_color(GOLD if corruption < 5 else BLOOD) + BOLD + f" {current_player}'S TURN ".center(cols) + RESET)
                move_cursor(1, rows // 2 + 1)
                print(get_color(GREY) + " (Target Numbers: 7, 11, or 13) ".center(cols) + RESET)
                
                move_cursor(cols // 2, rows - 1) # Position cursor near prompt
                if sys.stdin.readline().lower().strip() == 'q': raise KeyboardInterrupt
                
                v1, v2 = roll_physics_dice(corruption, current_player)
                total = v1 + v2
                time.sleep(0.5)
                clear_screen(); draw_ui(current_player, corruption)
                
                if total == 13 or v1 == 13 or v2 == 13:
                    effect_cursed_13(current_player)
                    player_data[current_player]["corruption"] = max(0, player_data[current_player]["corruption"] - 2)
                    continue

                move_cursor(1, rows // 2)
                res_col = BLOOD if (total in [7, 11]) else GOLD
                print(get_color(res_col) + BOLD + f" ▞ {v1} + {v2} = {total} ▚ ".center(cols) + RESET)
                time.sleep(1.5)

                if total in [7, 11]:
                    target = current_player
                    if len(ALL_PLAYERS) > 1:
                        clear_screen(); draw_ui(current_player, corruption)
                        move_cursor(1, rows // 3)
                        print(get_color(BLOOD) + BOLD + "!!! 7H3 V01D 0FF3R5 4 C0RRUP73D 61F7 !!!".center(cols) + RESET)
                        for i, p in enumerate(ALL_PLAYERS):
                            move_cursor(1, rows // 3 + 2 + i)
                            print(f"[{i+1}] {p} (Level: {player_data[p]['corruption']})".center(cols))
                        move_cursor(cols // 2 - 10, rows // 3 + 4 + len(ALL_PLAYERS))
                        print(get_color(GOLD) + "Blight: ", end="", flush=True)
                        try:
                            choice = int(sys.stdin.readline().strip()) - 1
                            if 0 <= choice < len(ALL_PLAYERS): target = ALL_PLAYERS[choice]
                        except: pass
                    player_data[target]["corruption"] += 1
                    corruption = player_data[target]["corruption"]
                    if target != current_player:
                        clear_screen(); draw_ui(current_player, corruption); move_cursor(1, rows // 2); print(get_color(BLOOD) + f"Y0U H4V3 BL16H73D {target}.".center(cols) + RESET); time.sleep(1.5)
                    if corruption == 1: move_cursor(1, rows // 2 + 2); print("F1R57 C0N74C7".center(cols)); time.sleep(1)
                    elif corruption == 2: effect_glitch(40)
                    elif corruption == 3: effect_melt(corruption)
                    elif corruption == 4: effect_system_breach(target, corruption)
                    elif corruption == 5: effect_static(30)
                    elif corruption >= 6:
                        choice = random.choice([effect_glitch, effect_melt, effect_system_breach, effect_static])
                        if choice == effect_system_breach: choice(target, corruption)
                        else: choice(corruption if choice == effect_melt else 20)
                        if corruption > 8:
                            effect_singularity(corruption)
                            move_cursor(1, rows // 2); print(get_color(BLOOD) + BOLD + BLINK + "R34L17Y C0LL4P53D. R380071N6...".center(cols) + RESET); time.sleep(3); player_data[target]["corruption"] = 0
                else:
                    if corruption > 0: move_cursor(1, rows // 2 + 2); print(f"LUCKY Y0U. 7H3 V01D 5P4R35 Y0U.".center(cols)); time.sleep(1)
    except (KeyboardInterrupt, EOFError):
        STALKER_ACTIVE = False
        clear_screen(); set_title("TH3 V01D N3V3R CL0535"); print(get_color(BLOOD) + "Y0U C4NN07 3X17 7H3 V01D.".center(cols)); time.sleep(1.5); print(SHOW_CURSOR)

if __name__ == "__main__": main()
