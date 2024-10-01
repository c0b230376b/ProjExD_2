import os 
import random
import sys
import pygame as pg
import time

# ゲーム画面の幅と高さを定義
WIDTH, HEIGHT = 1100, 650

# 移動の増分を定義（方向キーごとの移動量）
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

# 現在のディレクトリを設定（画像ファイル読み込み用）
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    物体（こうかとんや爆弾）が画面内に収まっているか確認する関数
    引数：こうかとん、または爆弾のRect
    戻り値：横方向、縦方向の判定結果のタプル（画面内ならTrue、画面外ならFalse）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface):
    """
    ゲームオーバー時に画面をブラックアウトし、「Game Over」を表示する関数。
    画面全体を黒くし、泣いているこうかとんの画像と「Game Over」の文字を5秒間表示する。
    引数：貼り付ける所
    戻り値はなし
    """
    kk_img_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  # 泣いているこうかとん画像
    kk_img_cry2 = pg.transform.flip(kk_img_cry, True, False)
    # 画面全体を半透明の黒で覆う
    black_surface = pg.Surface((WIDTH, HEIGHT))
    black_surface.set_alpha(128)  # 半透明度を設定
    black_surface.fill((100, 0, 0))  # 黒く塗りつぶす

    # フォントの設定（サイズ72）
    font = pg.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 255, 255))  # 白色で描画

    # 泣いているこうかとんの位置設定
    kk_rct_cry = kk_img_cry.get_rect()
    kk_rct_cry2 = kk_img_cry.get_rect()
    
    kk_rct_cry.center = WIDTH // 2 - 160, HEIGHT // 2
    kk_rct_cry2.center = WIDTH // 2 + 160, HEIGHT // 2

    # テキストの位置設定
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # 画面を更新
    screen.blit(black_surface, (0, 0))  # 半透明の黒い四角形を描画
    screen.blit(kk_img_cry, kk_rct_cry)  # 泣いているこうかとんの画像を描画
    screen.blit(kk_img_cry2, kk_rct_cry2)  # 泣いているこうかとんの画像を描画
    screen.blit(text, text_rect)  # 「Game Over」の文字を描画

    pg.display.update()  # 画面更新
    time.sleep(5)  # 5秒間表示
    print("Game_over")  # ターミナルに表示

def create_image_dict(kk_img: pg.Surface)-> dict:
    """
    こうかとんの画像を移動方向に応じて二倍になって回転させた辞書を返す関数。
    移動量の合計値タプルをキーに、rotozoomで回転させたSurfaceを値とした辞書を作成。
    引数：こうかとんの画像
    戻り値：こうかとんが飛ぶ方向に従ってこうかとん画像の辞書
    """
    image_dict = {
        #  画像rotozoom
        (5, 0): pg.transform.rotozoom(kk_img, -90, 1.0),   # 右
        (5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 右上
        (0, -5): pg.transform.rotozoom(kk_img, 0, 1.0),    # 上
        (-5, -5): pg.transform.rotozoom(kk_img, 45, 1.0),  # 左上
        (-5, 0): pg.transform.rotozoom(kk_img, 90, 1.0),   # 左
        (-5, 5): pg.transform.rotozoom(kk_img, 135, 1.0),  # 左下
        (0, 5): pg.transform.rotozoom(kk_img, 180, 1.0),   # 下
        (5, 5): pg.transform.rotozoom(kk_img, -135, 1.0),  # 右下
    }
    return image_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.image.load("fig/3.png")  # こうかとん画像

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の設定
    bb_img = pg.Surface((20, 20))  # 爆弾の表面
    bb_img.set_colorkey((0, 0, 0))  # 背景を透過
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    # こうかとんの回転画像の辞書を作成
    kk_img_dict = create_image_dict(kk_img)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])  # 背景を描画

        # こうかとんが爆弾と衝突した場合
        if kk_rct.colliderect(bb_rct):
            game_over(screen)  # ゲームオーバー画面を表示
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # キー入力に基づいてこうかとんを移動
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        # 移動があった場合、こうかとんの画像を移動方向に応じて変更
        if sum_mv != [0, 0]:    
            kk_img_rotated = kk_img_dict.get(tuple(sum_mv))  # 移動量に応じた画像を取得
        else:
            kk_img_rotated = kk_img  # 移動がなければ元の画像を使用

        kk_rct.move_ip(sum_mv)

        # 画面外に出ないように移動を制限
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  # 横方向の反転
        if not tate:
            vy *= -1  # 縦方向の反転

        screen.blit(kk_img_rotated, kk_rct)  # こうかとんを描画
        bb_rct.move_ip(vx, vy)  # 爆弾を移動
        screen.blit(bb_img, bb_rct)  # 爆弾を描画

        pg.display.update()  # 画面更新
        tmr += 1
        clock.tick(50)  # 50FPS

if __name__ == "__main__":
    pg.init()  # pygameの初期化
    main()
    pg.quit()  # pygameの終了
    sys.exit()  # プログラム
