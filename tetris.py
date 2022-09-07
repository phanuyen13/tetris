from tkinter import *
from tkinter import messagebox as msgbox
import platform
import threading
import multiprocessing
import os
from random import randint as rnd

vertical = 20  # 基盤の縦のマス数
side = 10  # 基盤の横のマス数
size = 30  # 1マスの大きさ
mino_size = 4  # ミノの(縦横最大の)ブロック数
form = 0  # ミノの種類
mode = 0  # ミノの向き
y = -1  # ミノのy座標
x = 4  # ミノのx座標
speed = 500  # 落下速度
y_data = [0, 0, 0, 0]
x_data = [0, 0, 0, 0]
foundation_data = [7, 7, 7, 7]
score = 0  # 得点

# 色の定義
colors = ["#00ffff",  # I:0
          "#0000ff",  # J:1
          "#ffa500",  # L:2
          "#ffff00",  # O:3
          "#008000",  # S:4
          "#800080",  # T:5
          "#ff0000",  # Z:6
          "#404040"]  # foundation:7

foundation = [[7 for i in range(side + 2)] for j in range(vertical + 2)]
for i in range(vertical + 2):
    foundation[i][0], foundation[i][side + 1] = 8, 8
foundation[vertical + 1] = [8 for i in range(side + 2)]

mino_data = [[[[2, 0], [2, 1], [2, 2], [2, 3]],  # I:0
              [[0, 1], [1, 1], [2, 1], [3, 1]],
              [[1, 0], [1, 1], [1, 2], [1, 3]],
              [[0, 2], [1, 2], [2, 2], [3, 2]]],
             [[[1, 0], [2, 0], [2, 1], [2, 2]],  # J:1
              [[1, 1], [1, 2], [2, 1], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 2]],
              [[1, 1], [2, 1], [3, 0], [3, 1]]],
             [[[1, 2], [2, 0], [2, 1], [2, 2]],  # L:2
              [[1, 1], [2, 1], [3, 1], [3, 2]],
              [[2, 0], [2, 1], [2, 2], [3, 0]],
              [[1, 0], [1, 1], [2, 1], [3, 1]]],
             [[[1, 1], [1, 2], [2, 1], [2, 2]],  # O:3
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]]],
             [[[1, 1], [1, 2], [2, 0], [2, 1]],  # S:4
              [[1, 1], [2, 1], [2, 2], [3, 2]],
              [[2, 1], [2, 2], [3, 0], [3, 1]],
              [[1, 0], [2, 0], [2, 1], [3, 1]]],
             [[[1, 1], [2, 0], [2, 1], [2, 2]],  # T:5
              [[1, 1], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 1]],
              [[1, 1], [2, 0], [2, 1], [3, 1]]],
             [[[1, 0], [1, 1], [2, 1], [2, 2]],  # Z:6
              [[1, 2], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [3, 1], [3, 2]],
              [[1, 1], [2, 0], [2, 1], [3, 0]]]]
mino = [[7 for i in range(mino_size)] for j in range(mino_size)]


def draw_foundation():
    for v in range(vertical):
        v1 = v * size
        v2 = v1 + size
        for s in range(side):
            s1 = s * size
            s2 = s1 + size
            for c in range(len(colors)):
                if foundation[v + 1][s + 1] == c:
                    color = colors[c]
                    cv.create_rectangle(s1, v1, s2, v2, fill=color)  # 四角形を描画



def create_mino():
    global form, mino
    form = rnd(0, 6)
    for i in range(len(mino_data[form][mode % 4])):
        y = mino_data[form][mode % 4][i][0]
        x = mino_data[form][mode % 4][i][1]
        mino[y][x] = form


def draw_mino():
    for v in range(mino_size):
        v1 = (v + y - 1) * size
        v2 = v1 + size
        for s in range(mino_size):
            s1 = (s + x - 1) * size
            s2 = s1 + size
            if mino[v][s] == form:
                cv.create_rectangle(s1, v1, s2, v2, fill=colors[form])


class Move_mino:
    def __init__(self, next_y, next_x, next_mode):
        self.next_y = next_y
        self.next_x = next_x
        self.next_mode = next_mode

    def reference(self):
        global x_data, y_data, foundation_data
        for i in range(len(mino_data[form][mode % 4])):
            y_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][0] + y
            x_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][1] + x
            foundation_data[i] = foundation[y_data[i] +
                                            self.next_y][x_data[i] + self.next_x]

    def move_mino(self, e):
        global x, y
        self.reference()
        if foundation_data == [7, 7, 7, 7]:
            y += 1 * self.next_y
            x += 1 * self.next_x
        cv.delete("all")  # キャンバス描画の消去
        global foundation, mino, mode
        if self.next_y == 1 and foundation_data != [7, 7, 7, 7]:
            for i in range(len(y_data)):
                foundation[y_data[i]][x_data[i]] = form
            delete()
            game_over()
            mode = 0
            y = -1
            x = 4
            mino = [[7 for i in range(mino_size)] for j in range(mino_size)]
            create_mino()
        draw_foundation()
        draw_mino()

    def drop_mino(self):
        global speed
        self.move_mino(Event)
        win.after(speed, self.drop_mino)

    def spin_mino(self, e):
        self.reference()
        global mode, mino
        if foundation_data == [7, 7, 7, 7]:
            mode += 1 * self.next_mode
            mino = [[7 for i in range(mino_size)] for j in range(mino_size)]
            for i in range(len(mino_data[form][mode % 4])):
                y = mino_data[form][mode % 4][i][0]
                x = mino_data[form][mode % 4][i][1]
                mino[y][x] = form
            cv.delete("all")
            draw_foundation()
            draw_mino()


def delete():
    global score, speed
    for v in range(len(foundation)):
        if (7 in foundation[v]) == False and foundation[v] != [8 for i in range(side + 2)]:
            del foundation[v]
            add_foundation = [7 for i in range(side + 2)]
            add_foundation[0], add_foundation[side + 1] = 8, 8
            foundation.insert(0, add_foundation)
            score += 1
            if speed > 50:
                speed -= 10
            score_label["text"] = f"Score: {score}"
            speed_label["text"] = f"Speed Level: {1+(500-speed)//50}"


def game_over():
    top_foundation = [7 for i in range(side + 2)]
    top_foundation[0], top_foundation[side + 1] = 8, 8
    if foundation[1] != top_foundation:
        msgbox.showinfo(message=f"Game Over\nScore: {score}")  # メッセージの表示
        if platform.system() == "Darwin":
            os.system("killall afplay")
        quit()
def create_win():
    win = Tk()  # ウィンドウの作成
    win.title("Tetris")
    return win
def draw_canvas():
    global cv
    cv = Canvas(win, width=side * size, height=vertical * size)  # キャンバスの作成
    cv.pack()
def create_labelscore(win):
    global score_label
    score_label = Label(win, text=f"Score: {score}", font=("", 20))
    score_label.place(x=side * size // 2, y=vertical * size)
    score_label.pack(anchor="center")
def create_speedlabel(win):
    global speed_label
    speed_label = Label(win, text=f"Speed Level: 1", font=("", 20))
    speed_label.place(x=side * size // 2, y=vertical * size + 20)
    speed_label.pack(anchor="center")
def tap_move_mino(win,tapkey,tapstring):
    win.bind(tapstring, tapkey.move_mino)
def tap_spin(win,tapkey,tapstring):
    win.bind(tapstring, tapkey.spin_mino)
def game():
    print("game starting...")
    global win
    win =create_win()
    draw_canvas()
    create_labelscore(win)
    create_speedlabel(win)
    create_mino()
    left = Move_mino(0, -1, 0)
    right = Move_mino(0, 1, 0)
    under = Move_mino(1, 0, 0)
    left_spin = Move_mino(0, 0, -1)
    right_spin = Move_mino(0, 0, 1)

    tap_move_mino(win,left,"<Left>")
    tap_move_mino(win, right, "<Right>")
    tap_move_mino(win, under, "<Return>")
    tap_spin(win,right_spin,"<Up>")
    tap_spin(win, left_spin, "<Down>")
    under.drop_mino()
    win.mainloop()
    print("game exit")


class MySound(threading.Thread):
    def __init__(self, file):
        super().__init__()
        self._file = file
        self.isDaemon = True
        self.running = True

    def run(self):
        print("play...")
        if platform.system() == "Windows":
            # Windowsの場合は、winsoundというPython標準ライブラリを使います.
            import winsound
            winsound.PlaySound(self._file, winsound.SND_FILENAME |
                               winsound.SND_ASYNC | winsound.SND_LOOP)


def play_bgm():
    bgm_file = "bgm.wav"
    print("play...")
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.PlaySound(bgm_file, winsound.SND_FILENAME |
                           winsound.SND_ASYNC | winsound.SND_LOOP)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        while 1:
            os.system("afplay " + bgm_file)


def play_game_over():
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.PlaySound("game_over.wav", winsound.SND_FILENAME)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        os.system("afplay " + "game_over.wav")


def main():
    # t1 = threading.Thread(target=game)
    # t2 = MySound("bgm.wav")
    # bgm = multiprocessing.Process(target=play_bgm)
    # # t1.start()
    # bgm.start()
    game()
    # if platform.system() == "Darwin":
    #     os.system("killall afplay")
    # bgm.terminate()
    # play_game_over()
    # print("finished all")
    # t1.join()


if __name__ == "__main__":
    main()
