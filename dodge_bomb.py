import os 
import random
import sys
import pygame as pg
import time  # 追加

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

def game_over(screen, kk_img_cry):
    """
    ゲームオーバー時に画面をブラックアウトし、「Game Over」を表示する関数。
    画面全体を黒くし、泣いているこうかとんの画像と「Game Over」の文字を5秒間表示する。
    """
    # 画面全体を半透明の黒で覆う
    black_surface = pg.Surface((WIDTH, HEIGHT))
    black_surface.set_alpha(128)  # 半透明度を設定
    black_surface.fill((0, 0, 0))  # 黒く塗りつぶす

    # フォントの設定（サイズ72）
    font = pg.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 255, 255))  # 白色で描画

    # 泣いているこうかとんの位置設定
    kk_rct_cry = kk_img_cry.get_rect()
    kk_rct_cry.center = WIDTH // 2, HEIGHT // 2

    # テキストの位置設定
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # 画面を更新
    screen.blit(black_surface, (0, 0))  # 半透明の黒い四角形を描画
    screen.blit(kk_img_cry, kk_rct_cry)  # 泣いているこうかとんの画像を描画
    screen.blit(text, text_rect)  # 「Game Over」の文字を描画

    pg.display.update()  # 画面更新
    time.sleep(5)  # 5秒間表示

def main():
    pg.display.set_caption("逃げろ！こうかとん")  # ゲームウィンドウのタイトル
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ゲームウィンドウのサイズ
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとん画像
    kk_img_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  # 泣いているこうかとん画像

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の設定
    bb_img = pg.Surface((20, 20))  # 爆弾の表面
    bb_img.set_colorkey((0, 0, 0))  # 背景を透過
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾を描画
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])  # 背景を描画

        # こうかとんが爆弾と衝突した場合
        if kk_rct.colliderect(bb_rct):
            game_over(screen, kk_img_cry)  # ゲームオーバー画面を表示
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # キー入力に基づいてこうかとんを移動
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)

        # 画面外に出ないように移動を制限
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  # 横方向の反転
        if not tate:
            vy *= -1  # 縦方向の反転

        screen.blit(kk_img, kk_rct)  # こうかとんを描画
        bb_rct.move_ip(vx, vy)  # 爆弾を移動
        screen.blit(bb_img, bb_rct)  # 爆弾を描画

        pg.display.update()  # 画面更新
        tmr += 1
        clock.tick(50)  # 50FPS

if __name__ == "__main__":
    pg.init()  # pygameの初期化
    main()
    pg.quit()  # pygameの終了
    sys.exit()  # プログラムの終了
