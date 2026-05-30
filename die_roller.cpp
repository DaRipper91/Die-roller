#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <random>
#include <cmath>
#include <sys/ioctl.h>
#include <unistd.h>
#include <atomic>
#include <algorithm>

using namespace std;

// --- CONFIG & COLORS ---
const vector<int> RAINBOW = {196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 47, 48, 49, 50, 51, 45, 39, 33, 27, 21, 57, 93, 129, 165, 201, 200, 199, 198, 197};
const int GOLD = 220;
const int WHITE = 255;
const int GREY = 240;
const int BLOOD = 124;
const int VOID_COLOR = 232;
const string RESET = "\033[0m";
const string BOLD = "\033[1m";
const string BLINK = "\033[5m";
const string HIDE_CURSOR = "\033[?25l";
const string SHOW_CURSOR = "\033[?25h";

atomic<bool> STALKER_ACTIVE(true);
atomic<int> CORRUPTION_LEVEL(0);

string get_color(int code) {
    return "\033[38;5;" + to_string(code) + "m";
}

string get_bg(int code) {
    return "\033[48;5;" + to_string(code) + "m";
}

void clear_screen() {
    cout << "\033[H\033[J" << flush;
}

struct TermSize {
    int cols, rows;
};

TermSize get_terminal_size() {
    struct winsize w;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
    return {w.ws_col, w.ws_row};
}

void move_cursor(int x, int y) {
    cout << "\033[" << y << ";" << x << "H";
}

// --- THE STALKER ---
void stalker_loop() {
    vector<string> whispers = {
        "I SEE YOU.", "ROLL AGAIN.", "WHY DO YOU PERSIST?", 
        "THE VOID HUNGERS.", "SIX. SIX. SIX.", "IT IS INEVITABLE.",
        "HE IS COMING.", "DON'T LOOK BEHIND YOU.", "01100110"
    };
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);

    while (STALKER_ACTIVE) {
        if (CORRUPTION_LEVEL > 2 && dis(gen) < (0.05 * CORRUPTION_LEVEL)) {
            TermSize ts = get_terminal_size();
            uniform_int_distribution<> dis_x(1, max(1, ts.cols - 15));
            uniform_int_distribution<> dis_y(1, max(1, ts.rows));
            uniform_int_distribution<> dis_w(0, whispers.size() - 1);

            int x = dis_x(gen);
            int y = dis_y(gen);
            string phrase = whispers[dis_w(gen)];

            printf("\033[s\033[%d;%dH%s%s%s\033[u", y, x, get_color(BLOOD).c_str(), phrase.c_str(), RESET.c_str());
            fflush(stdout);
        }
        this_thread::sleep_for(chrono::milliseconds(500 + (int)(dis(gen) * 1500)));
    }
}

// --- NIGHTMARE PAYLOADS ---

void effect_static(int duration = 15) {
    TermSize ts = get_terminal_size();
    string chars = " .:-=+*#%@";
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis_c(0, chars.length() - 1);
    uniform_int_distribution<> dis_color(0, 23);
    uniform_real_distribution<> dis_p(0, 1);

    for (int i = 0; i < duration; ++i) {
        clear_screen();
        string screen = "";
        for (int y = 0; y < ts.rows; ++y) {
            string line = "";
            for (int x = 0; x < ts.cols; ++x) {
                if (dis_p(gen) > 0.05) line += chars[dis_c(gen)];
                else line += "6";
            }
            screen += get_color(232 + dis_color(gen)) + line + RESET + "\n";
        }
        cout << screen << flush;
        this_thread::sleep_for(chrono::milliseconds(40));
    }
}

void effect_glitch(int duration = 20) {
    TermSize ts = get_terminal_size();
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis_off(-5, 5);
    uniform_int_distribution<> dis_row(1, ts.rows);
    uniform_int_distribution<> dis_r(0, RAINBOW.size() - 1);

    for (int i = 0; i < duration; ++i) {
        int offset = dis_off(gen);
        int row = dis_row(gen);
        move_cursor(1, row);
        cout << "\033[2K";
        int abs_off = abs(offset);
        for(int j=0; j<abs_off; ++j) cout << " ";
        cout << get_color(RAINBOW[dis_r(gen)]);
        for(int j=0; j<(ts.cols - abs_off); ++j) cout << "█";
        cout << RESET << flush;
        this_thread::sleep_for(chrono::milliseconds(10));
    }
}

void effect_melt(int level) {
    TermSize ts = get_terminal_size();
    string chars = "66680&%$#@!?";
    vector<vector<string>> screen(ts.rows, vector<string>(ts.cols, " "));
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);
    uniform_int_distribution<> dis_c(0, chars.length() - 1);

    for (int i = 0; i < 30 + level * 10; ++i) {
        clear_screen();
        for (int y = ts.rows - 1; y > 0; --y) {
            for (int x = 0; x < ts.cols; ++x) {
                if (screen[y - 1][x] != " " && dis(gen) < 0.4) {
                    screen[y][x] = screen[y - 1][x];
                    screen[y - 1][x] = " ";
                }
            }
        }
        for (int x = 0; x < ts.cols; ++x) {
            if (dis(gen) < 0.05) {
                screen[0][x] = get_color(BLOOD) + "▼" + RESET;
            }
        }
        string output = "";
        for (auto& row : screen) {
            for (auto& cell : row) output += cell;
            output += "\n";
        }
        cout << output << flush;
        this_thread::sleep_for(chrono::milliseconds(50));
    }
}

void effect_system_breach(int level) {
    TermSize ts = get_terminal_size();
    vector<string> fake_logs = {
        "CRITICAL_FAILURE: reality_engine.so not found",
        "SEGMENTATION FAULT AT ADDRESS 0x66666666",
        "WARNING: MEMORY LEAK IN human_consciousness_subsystem",
        "INJECTING CORE_VOID.DLL...",
        "PARSING SOUL_DATA... DONE.",
        "ERROR: USER_NOT_FOUND",
        "REBOOTING UNIVERSE IN 3... 2... 1..."
    };
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0, 1);
    uniform_int_distribution<> dis_l(0, fake_logs.size() - 1);
    uniform_int_distribution<> dis_c(0, 23);

    for (int i = 0; i < level * 5; ++i) {
        clear_screen();
        for (int y = 0; y < ts.rows; ++y) {
            if (dis(gen) < 0.2) {
                cout << get_color(160) << fake_logs[dis_l(gen)] << RESET << endl;
            } else {
                string hex_line = "";
                for (int x = 0; x < ts.cols; ++x) {
                    hex_line += "0123456789ABCDEF"[gen() % 16];
                }
                cout << get_color(232 + dis_c(gen)) << hex_line << RESET << endl;
            }
        }
        this_thread::sleep_for(chrono::milliseconds(100));
    }
}

void effect_singularity(int level) {
    TermSize ts = get_terminal_size();
    int cx = ts.cols / 2;
    int cy = ts.rows / 2;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis_r(0, RAINBOW.size() - 1);

    for (int r = 1; r < max(ts.cols, ts.rows); ++r) {
        clear_screen();
        string screen = "";
        for (int y = 0; y < ts.rows; ++y) {
            for (int x = 0; x < ts.cols; ++x) {
                double dist = sqrt(pow(x - cx, 2) + pow(y * 2 - cy * 2, 2));
                if (abs(dist - r) < 2) {
                    screen += get_color(RAINBOW[dis_r(gen)]) + "6" + RESET;
                } else if (dist < r) {
                    screen += get_bg(VOID_COLOR + ((int)dist % 10)) + " " + RESET;
                } else {
                    screen += " ";
                }
            }
            screen += "\n";
        }
        cout << screen << flush;
        this_thread::sleep_for(chrono::milliseconds(20));
    }
}

void effect_moo_level(int duration = 50) {
    TermSize ts = get_terminal_size();
    vector<string> cow = {
        " ^__^",
        " (oo)\\_______",
        " (__)\\       )\\/\\",
        "     ||----w |",
        "     ||     ||"
    };

    struct MooCow {
        float x, y, vx;
        int color;
    };

    vector<MooCow> cows;
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis_x(-20, ts.cols);
    uniform_real_distribution<> dis_y(0, ts.rows - 5);
    uniform_real_distribution<> dis_vx(0.5, 2.0);
    uniform_int_distribution<> dis_r(0, RAINBOW.size() - 1);

    for (int i = 0; i < 10; ++i) {
        cows.push_back({(float)dis_x(gen), (float)dis_y(gen), (float)dis_vx(gen), RAINBOW[dis_r(gen)]});
    }

    for (int i = 0; i < duration; ++i) {
        clear_screen();
        string screen_buf = "";
        vector<vector<string>> grid(ts.rows, vector<string>(ts.cols, " "));

        // Rainbow Static Background
        for (int y = 0; y < ts.rows; ++y) {
            for (int x = 0; x < ts.cols; ++x) {
                if ((rand() % 100) < 30) {
                    grid[y][x] = get_color(RAINBOW[rand() % RAINBOW.size()]) + "█" + RESET;
                }
            }
        }

        // Cows
        for (auto& c : cows) {
            for (int ry = 0; ry < 5; ++ry) {
                for (int rx = 0; rx < cow[ry].length(); ++rx) {
                    int tx = (int)c.x + rx;
                    int ty = (int)c.y + ry;
                    if (tx >= 0 && tx < ts.cols && ty >= 0 && ty < ts.rows) {
                        grid[ty][tx] = get_color(c.color) + BOLD + cow[ry][rx] + RESET;
                    }
                }
            }
            c.x += c.vx;
            if (c.x > ts.cols) c.x = -20;
        }

        for (int y = 0; y < ts.rows; ++y) {
            for (int x = 0; x < ts.cols; ++x) {
                screen_buf += grid[y][x];
            }
            screen_buf += "\n";
        }
        cout << screen_buf << flush;
        this_thread::sleep_for(chrono::milliseconds(50));
    }
}

// --- CORE LOGIC ---

vector<string> get_3d_die(int n, int color_code, bool glitch = false) {
    static vector<vector<string>> faces = {
        {"     ", "  ●  ", "     "},
        {"●    ", "     ", "    ●"},
        {"●    ", "  ●  ", "    ●"},
        {"●   ●", "     ", "●   ●"},
        {"●   ●", "  ●  ", "●   ●"},
        {"●   ●", "●   ●", "●   ●"}
    };
    
    vector<string> rows = faces[n - 1];
    if (glitch) {
        for (auto& row : rows) {
            for (auto& c : row) {
                if ((rand() % 100) < 20) c = '6';
            }
        }
    }

    string c = get_color(color_code) + BOLD;
    string g = get_color(GREY);
    
    return {
        c + "  ╔═══════╗" + RESET,
        c + "  ║ " + rows[0] + " ║" + g + "╗" + RESET,
        c + "  ║ " + rows[1] + " ║" + g + "║" + RESET,
        c + "  ║ " + rows[2] + " ║" + g + "║" + RESET,
        c + "  ╚═══════╝" + g + "║" + RESET,
        g + "   ╚═══════╝" + RESET
    };
}

void center_print(const vector<string>& lines) {
    TermSize ts = get_terminal_size();
    int v_pad = (ts.rows - (int)lines.size()) / 2;
    for (int i = 0; i < v_pad; ++i) cout << endl;
    for (const string& line : lines) {
        int h_pad = (ts.cols - 11) / 2;
        for (int i = 0; i < h_pad; ++i) cout << " ";
        cout << line << endl;
    }
}

void roll_animation(int level) {
    int frames = 10 + (level * 5);
    for (int i = 0; i < frames; ++i) {
        clear_screen();
        int res = (rand() % 6) + 1;
        bool is_glitched = (rand() % 100) < (level * 10);
        int color = is_glitched ? RAINBOW[rand() % RAINBOW.size()] : WHITE;
        center_print(get_3d_die(res, color, is_glitched));
        cout << flush;
        this_thread::sleep_for(chrono::milliseconds(50));
    }
}

int main() {
    srand(time(0));
    int corruption = 0;
    cout << HIDE_CURSOR << flush;

    thread stalker(stalker_loop);

    try {
        while (true) {
            CORRUPTION_LEVEL = corruption;
            TermSize ts = get_terminal_size();
            clear_screen();

            string header = " CORRUPTION LEVEL: " + to_string(corruption) + " ";
            if (corruption > 0) {
                for (auto& c : header) {
                    if ((rand() % 100) < (5 * corruption)) c = '6';
                }
            }

            for (int i = 0; i < ts.rows / 4; ++i) cout << endl;
            int h_pad = (ts.cols - (int)header.length()) / 2;
            for (int i = 0; i < h_pad; ++i) cout << " ";
            cout << get_color(corruption < 5 ? GOLD : BLOOD) << BOLD << header << RESET << endl;

            string prompt = "[ PRESS ENTER TO ROLL YOUR FATE ]";
            h_pad = (ts.cols - (int)prompt.length()) / 2;
            for (int i = 0; i < h_pad; ++i) cout << " ";
            cout << get_color(GREY) << prompt << RESET << endl;

            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            roll_animation(corruption);
            int result = (rand() % 6) + 1;

            if (corruption > 10 && (rand() % 100) < 30) result = 6;

            clear_screen();
            int color = (result == 6) ? GOLD : WHITE;
            if (corruption > 5 && result == 6) color = BLOOD;

            center_print(get_3d_die(result, color, corruption > 3));
            cout << flush;
            this_thread::sleep_for(chrono::milliseconds(800));

            if (result == 6) {
                corruption++;
                if (corruption == 1) {
                    string msg = "FIRST CONTACT";
                    int m_pad = (ts.cols - (int)msg.length()) / 2;
                    cout << endl;
                    for (int i = 0; i < m_pad; ++i) cout << " ";
                    cout << msg << endl;
                    this_thread::sleep_for(chrono::seconds(1));
                } else if (corruption == 2) effect_glitch(40);
                else if (corruption == 3) effect_melt(corruption);
                else if (corruption == 4) effect_system_breach(corruption);
                else if (corruption == 5) effect_static(30);
                else if (corruption == 6) effect_moo_level(60);
                else if (corruption >= 7) {
                    effect_glitch(20);
                    effect_system_breach(2);
                    effect_static(10);
                    effect_moo_level(20);
                    effect_singularity(corruption);
                    if (corruption > 10) {
                        string reboot = "REALITY COLLAPSED. REBOOTING...";
                        int r_pad = (ts.cols - (int)reboot.length()) / 2;
                        cout << get_color(BLOOD) << BOLD << BLINK;
                        for (int i = 0; i < r_pad; ++i) cout << " ";
                        cout << reboot << RESET << endl;
                        this_thread::sleep_for(chrono::seconds(3));
                        corruption = 0;
                    }
                }
            } else {
                if (corruption > 0) {
                    string lucky = "LUCKY YOU. IT WAS A " + to_string(result) + ".";
                    int l_pad = (ts.cols - (int)lucky.length()) / 2;
                    cout << endl;
                    for (int i = 0; i < l_pad; ++i) cout << " ";
                    cout << lucky << endl;
                }
                this_thread::sleep_for(chrono::seconds(1));
            }
        }
    } catch (...) {
        STALKER_ACTIVE = false;
        stalker.join();
        clear_screen();
        TermSize ts = get_terminal_size();
        string bye = "YOU CANNOT EXIT THE VOID.";
        int b_pad = (ts.cols - (int)bye.length()) / 2;
        for (int i = 0; i < b_pad; ++i) cout << " ";
        cout << get_color(BLOOD) << bye << RESET << endl;
        this_thread::sleep_for(chrono::seconds(1));
        cout << SHOW_CURSOR << flush;
    }

    return 0;
}
