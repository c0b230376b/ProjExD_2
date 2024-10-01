import os  # 导入操作系统相关模块
import sys  # 导入系统相关模块
import pygame as pg  # 导入pygame模块并简化命名为pg
import random  # 导入随机数模块

# 定义屏幕的宽度和高度
WIDTH, HEIGHT = 1100, 650
# 设置当前工作目录为脚本所在的目录，以便加载资源文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定义键盘按键与移动量之间的对应关系
DELTA = {
    pg.K_UP: (0, -5),     # 上箭头：Y坐标减少5
    pg.K_DOWN: (0, 5),    # 下箭头：Y坐标增加5
    pg.K_LEFT: (-5, 0),   # 左箭头：X坐标减少5
    pg.K_RIGHT: (5, 0)    # 右箭头：X坐标增加5
}

def check_bound(obj_rct):
    """检查物体是否在屏幕范围内的函数"""
    yoko, tate = True, True  # 初始假设物体在屏幕内
    # 检查物体是否越过屏幕的左右边界
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        yoko = False  # 物体在横向越界
    # 检查物体是否越过屏幕的上下边界
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False  # 物体在纵向越界
    return yoko, tate  # 返回横向和纵向的边界判断结果

def main():
    """游戏的主函数"""
    pg.display.set_caption("逃げろ！こうかとん")  # 设置窗口标题
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 创建游戏窗口
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 加载背景图片
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # 加载并缩放こうかとん的图片
    kk_rct = kk_img.get_rect()  # 获取こうかとん的矩形区域
    kk_rct.center = 300, 200  # 设置こうかとん的初始位置

    # 创建爆弾（炸弹）的Surface，并设置为红色圆形
    bb_img = pg.Surface((20, 20))  # 创建一个20x20的Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 在Surface上绘制一个红色圆形
    bb_img.set_colorkey((0, 0, 0))  # 设置黑色部分为透明
    bb_rct = bb_img.get_rect()  # 获取爆弾的矩形区域
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 随机设置爆弾的位置

    vx, vy = 5, 5  # 定义爆弾的移动速度（x方向和y方向均为5）

    clock = pg.time.Clock()  # 创建时钟对象用于控制帧率
    while True:  # 游戏主循环
        for event in pg.event.get():  # 处理事件
            if event.type == pg.QUIT:  # 如果用户关闭窗口
                return  # 退出主函数

        screen.blit(bg_img, [0, 0])  # 在屏幕上绘制背景图片

        # 获取当前按键的状态
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 初始化移动量
        # 根据按键状态计算移动量
        for key, delta in DELTA.items():  # 遍历DELTA字典
            if key_lst[key]:  # 如果按下对应的键
                sum_mv[0] += delta[0]  # 累加x方向的移动量
                sum_mv[1] += delta[1]  # 累加y方向的移动量

        kk_rct.move_ip(sum_mv)  # 更新こうかとん的位置

        # 检查こうかとん是否越界
        yoko, tate = check_bound(kk_rct)
        if not yoko:  # 如果横向越界
            kk_rct.move_ip(-sum_mv[0], 0)  # 将横向移动量反向（恢复到上一个位置）
        if not tate:  # 如果纵向越界
            kk_rct.move_ip(0, -sum_mv[1])  # 将纵向移动量反向（恢复到上一个位置）

        # 移动爆弾
        bb_rct.move_ip(vx, vy)

        # 检查爆弾是否越界
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 如果横向越界
            vx = -vx  # 反转爆弾在x方向的速度
        if not tate:  # 如果纵向越界
            vy = -vy  # 反转爆弾在y方向的速度

        screen.blit(kk_img, kk_rct)  # 在屏幕上绘制こうかとん
        screen.blit(bb_img, bb_rct)  # 在屏幕上绘制爆弾

        # 检查碰撞
        if kk_rct.colliderect(bb_rct):  # 如果こうかとん与爆弾发生碰撞
            return  # 结束游戏（返回到主函数）

        pg.display.update()  # 更新显示
        clock.tick(50)  # 控制帧率为50帧每秒

if __name__ == "__main__":
    pg.init()  # 初始化pygame
    main()  # 调用主函数
    pg.quit()  # 退出pygame
    sys.exit()  # 结束程序
