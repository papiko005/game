# pygameを読み込む
import pygame
# player.pyのPlayerクラスを読み込む
from player import Player
# enemies.pyの変数、関数、クラス全てを読み込む
from enemies import *
# GUI作成ライブラリtkinterを読み込む
import tkinter
# GUI作成ライブラリtkinterのmessagebox関数を読み込む
from tkinter import messagebox  

# 画面のサイズ
SCREEN_WIDTH = 1100   
SCREEN_HEIGHT = 800

# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

class Game(object):
    """
    Gameクラス
    """
    def __init__(self):
        """
        初期化関数
        """
        # フォント読み込み
        self.font = pygame.font.Font(None,40)
        # Ruluフラグ
        self.rulus = False
        # ゲームオーバーフラグ
        self.game_over = True
        # ゲームクリアフラグ
        self.game_clear = True
        # スコア
        self.score = 0
        # フォント
        self.font = pygame.font.Font(None,35)

        # メニューを設定。後述のMenuクラスを初期化
        self.menu = Menu(("Start","Rulu","Exit"),font_color = WHITE,font_size=60)
        # プレイヤーを初期化
        self.player = Player(32,128,"img/Runman.png")
        
        # 水平ブロック(なし)
        self.horizontal_blocks = pygame.sprite.Group()
        # 垂直方向のブロック(なし)
        self.vertical_blocks = pygame.sprite.Group()

        # ドットのグループ(なし)
        self.dots_group = pygame.sprite.Group()

        # ブロックの描画(なし)
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))

        # 敵を定義
        self.enemies = pygame.sprite.Group()
        # 敵を追加。初期位置と移動座標を引数に渡す
        self.enemies.add(Yuurei(288,96,0,2))
        self.enemies.add(Yuurei(288,320,0,-2))
        self.enemies.add(Yuurei(544,128,0,2))
        self.enemies.add(Yuurei(32,224,0,2))
        self.enemies.add(Yuurei(160,64,2,0))
        self.enemies.add(Yuurei(448,64,-2,0))
        self.enemies.add(Yuurei(640,448,2,0))
        self.enemies.add(Yuurei(448,320,2,0))
        self.enemies.add(Yuurei(189,432,2,0))
        self.enemies.add(Yuurei(256,256,3,-2))
        self.enemies.add(Yuurei(19,40,1,-2))
        self.enemies.add(Yuurei(6,341,-3,3))
        self.enemies.add(Yuurei(26,432,6,2))
        self.enemies.add(Yuurei(266,654,3,6))
        self.enemies.add(Yuurei(888,733,5,2))
        self.enemies.add(Yuurei(600,921,8,3))
        self.enemies.add(Yuurei(511,787,3,0))
        self.enemies.add(Yuurei(611,821,5,-8))
        self.enemies.add(Yuurei(711,843,2,-3))
        self.enemies.add(Yuurei(511,922,1,4))
        self.enemies.add(Yuurei(911,14,-6,-5))

    def process_events(self):
        """
        キー操作
        """

        for event in pygame.event.get(): 
            # QUIT状態になったらゲーム終了
            if event.type == pygame.QUIT: 
                return True
            # メニューの操作
            self.menu.event_handler(event)
            # キー判定
            if event.type == pygame.KEYDOWN:
                # リターンキー（エンターキー）を押した
                if event.key == pygame.K_RETURN:
                    # ゲームオーバーの状態かつRulusフラグがFalse
                    if self.game_over and not self.rulus:
                        # Startを選択
                        if self.menu.state == 0:
                            # 初期化
                            self.__init__()
                            # ゲームオーバーフラグを戻す
                            self.game_over = False
                        # Rulusを選択
                        elif self.menu.state == 1:
                            self.rulus = True
                        # Quitを選択
                        elif self.menu.state == 2:
                            return True

                # 右矢印キーを押した
                elif event.key == pygame.K_RIGHT:
                    # プレイヤーが右に移動
                    self.player.move_right()
                # 左矢印キーを押した
                elif event.key == pygame.K_LEFT:
                    # プレイヤーが左に移動
                    self.player.move_left()
                # 上矢印を押した
                elif event.key == pygame.K_UP:
                    # プレイヤーが上に移動
                    self.player.move_up()
                # 下矢印を押した
                elif event.key == pygame.K_DOWN:
                    # プレイヤーが下に移動
                    self.player.move_down()
                # ESCキーを押した
                elif event.key == pygame.K_ESCAPE:
                    # ゲームオーバー
                    self.game_over = True
                    self.rulus = False

            # 指をキーを離した
            elif event.type == pygame.KEYUP:
                # 右矢印キーを離した
                if event.key == pygame.K_RIGHT:
                    # 右移動を停止
                    self.player.stop_move_right()
                # 左矢印キーを離した
                elif event.key == pygame.K_LEFT:
                    # 左移動を停止
                    self.player.stop_move_left()
                # 上矢印キーを離した
                elif event.key == pygame.K_UP:
                    # 上移動を停止
                    self.player.stop_move_up()
                # 下矢印キーを離した
                elif event.key == pygame.K_DOWN:
                    # 下移動を停止
                    self.player.stop_move_down()
             
        return False

    def run_logic(self):

        # ゲームオーバー状態ではない
        if not self.game_over:
            # プレイヤーをupdate
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            
            # プレイヤーと敵との衝突判定
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            
            if len(block_hit_list) > 0:
                # スコアを加算
                self.score += 1
            
            # 衝突した敵が1体以上いれば
            if len(block_hit_list) > 0:
                # プレイヤーの爆発フラグがTrueになる
                self.player.explosion = True

            # playerのゲームオーバーフラグを代入
            self.game_over = self.player.game_over
            # 敵をupdate
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)  

    def display_frame(self,screen):
        """
        ディスプレイ描画を管理
        """
        # 黒に塗りつぶして初期化
        screen.fill(BLACK)

        # ゲームオーバー状態
        if self.game_over:
            # Rulusを選択した
            if self.rulus:
                # メッセージをディスプレイに表示
                self.display_message(screen,"Use the arrow keys to escape from the ghost")
            else:
                self.menu.display_frame(screen)
        else:
            # 水平方向のブロックを描画(なし)
            self.horizontal_blocks.draw(screen)
            # 垂直方向のブロックを描画(なし)
            self.vertical_blocks.draw(screen)
            # ドットを描画(なし)
            self.dots_group.draw(screen)
            # 敵を描画
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)

            # スコアをテキスト表示
            text = self.font.render("second: " + str(self.score),True,BLUE)
            screen.blit(text,[120,20])
            
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,0,0)):
        """
        メッセージを描画をする
        """
        label = self.font.render(message,True,color)

        width = label.get_width()
        height = label.get_height()

        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)

        screen.blit(label,(posX,posY))


class Menu(object):
    """
    メニュー作成をするクラス
    """
    # メニューのインデックス
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,100,100),ttf_font=None,font_size=100):
        # デフォルトのテキストの色
        self.font_color = font_color
        # 選択時のテキストの色
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        """
        メニューのテキストを選択すると色が変わる
        """
        for index, item in enumerate(self.items):
            if self.state == index:
                # テキストを選択した
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        """
        メニューの選択
        """

        # キーを押した
        if event.type == pygame.KEYDOWN:
            # 上矢印きーを押した
            if event.key == pygame.K_UP:
                if self.state > 0:
                    # 上に移動
                    self.state -= 1
            # 下矢印キーを押した
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    # 下に移動
                    self.state += 1
