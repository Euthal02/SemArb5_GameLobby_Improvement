from pygame import init as pygame_init
from pygame import Rect as pygame_rect
from pygame.time import delay as pygame_delay

class PongGame:

    def __init__(self, socketio_object, user_session_object, flask_session):
        # init the game
        self.window_width = 800
        self.window_height = 600
        self.background_color = (255, 255, 255)
        self.paddle_width = 10
        self.paddle_height = 100
        self.ball_size = 20

        # logic params
        self.paddle_speed = 6.5
        self.ball_speed_x = 3.5
        self.ball_speed_y = 3.5
        self.socketio_object = socketio_object
        self.user_session_object = user_session_object
        self.flask_session = flask_session

        pygame_init()

        # create objects
        self.player1 = pygame_rect(10, ((self.window_height//2)-(self.paddle_height//2)), self.paddle_width, self.paddle_height)
        self.player2 = pygame_rect((self.window_width-20), ((self.window_height//2)-(self.paddle_height//2)), self.paddle_width, self.paddle_height)
        self.ball = pygame_rect(((self.window_width//2)-(self.ball_size//2)), ((self.window_height//2)-(self.ball_size//2)), self.ball_size, self.ball_size)

    def update(self):
        self.delay(30)
        if self.ball_speed_x != 3.5 and self.ball_speed_x != -3.5:
            print(self.ball_speed_x)
        # ball movement
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        # collision with edges
        if self.ball.top <= 0 or self.ball.bottom >= self.window_height:
            self.ball_speed_y *= -1
        # collision with paddles
        if self.ball.colliderect(self.player1) or self.ball.colliderect(self.player2):
            self.ball_speed_x *= -1
        # reset ball, upon scoring
        if self.ball.left <= 0 or self.ball.right >= self.window_width:
            self.ball.x = self.window_width // 2 - self.ball_size // 2
            self.ball.y = self.window_height // 2 - self.ball_size // 2
        # Spielzustand an den Client senden
        self.socketio_object.emit(
            'update', {
                'ball': {'x': self.ball.x, 'y': self.ball.y},
                'player1': {'x': self.player1.x, 'y': self.player1.y},
                'player2': {'x': self.player2.x, 'y': self.player2.y}
            }
        )     

    def game_move(self, move_data):
        sid = str(self.flask_session.get('sid'))

        if sid == self.user_session_object.all_user_sessions.get('player1') and move_data['direction']:
            if move_data['direction'] == 'up' and self.player1.top > 0:
                self.player1.y -= self.paddle_speed
            elif move_data['direction'] == 'down' and self.player1.bottom < self.window_height:
                self.player1.y += self.paddle_speed

        elif sid == self.user_session_object.all_user_sessions.get('player2') and move_data['direction']:
            if move_data['direction'] == 'up' and self.player2.top > 0:
                self.player2.y -= self.paddle_speed
            elif move_data['direction'] == 'down' and self.player2.bottom < self.window_height:
                self.player2.y += self.paddle_speed

    def delay(self, ms):
        pygame_delay(ms)
