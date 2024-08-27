import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

##############
##  Config  ##
##############

l = 20 # Robot looking left
r = 110 # Robot looking right
lr_center = 65 # Robot looking centered in the x-axis (x=0)

u = 108 # Robot looking up
d = 52 # Robot looking down
ud_center = 90 # Robot looking centered in the y-axis (y=0)

ud_center_r_eye_lower_eyelid_open = 45 # When y=0, right eye lower eyelid open
ud_center_r_eye_upper_eyelid_open = 85 # When y=0, right eye upper eyelid open

ud_center_r_eye_lower_eyelid_closed = 95 # When y=0, right eye lower eyelid closed (blink)
ud_center_r_eye_upper_eyelid_closed = 55 # When y=0, right eye upper eyelid closed (blink)

ud_center_l_eye_lower_eyelid_open = 115 # When y=0, left eye lower eyelid open
ud_center_l_eye_upper_eyelid_open = 60 # When y=0, left eye upper eyelid open

ud_center_l_eye_lower_eyelid_closed = 65 # When y=0, left eye lower eyelid closed (blink)
ud_center_l_eye_upper_eyelid_closed = 90 # When y=0, left eye upper eyelid closed (blink)

##############
##  Setup   ##
##############

# Initialize I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create a simple PCA9685 class instance
pca = PCA9685(i2c)
pca.frequency = 50

# Create servo objects for each eye function
lr_servo = servo.Servo(pca.channels[0])
ud_servo = servo.Servo(pca.channels[1])
left_eye_upper_eyelid = servo.Servo(pca.channels[2])
left_eye_lower_eyelid = servo.Servo(pca.channels[3])
right_eye_upper_eyelid = servo.Servo(pca.channels[4])
right_eye_lower_eyelid = servo.Servo(pca.channels[5])

###############
## Positions ##
###############

# When eyes look up, eyelids must move up accordingly

u_r_eye_lower_eyelid_open = ud_center_r_eye_lower_eyelid_open + (u - ud_center) # (With eyes looking) up: right eye lower eyelid open
u_r_eye_upper_eyelid_open = ud_center_r_eye_upper_eyelid_open + (u - ud_center)

u_r_eye_lower_eyelid_closed = ud_center_r_eye_lower_eyelid_closed + (u - ud_center)
u_r_eye_upper_eyelid_closed = ud_center_r_eye_upper_eyelid_closed + (u - ud_center)

u_l_eye_lower_eyelid_open = ud_center_l_eye_lower_eyelid_open - (u - ud_center)
u_l_eye_upper_eyelid_open = ud_center_l_eye_upper_eyelid_open - (u - ud_center)

u_l_eye_lower_eyelid_closed = ud_center_l_eye_lower_eyelid_closed - (u - ud_center)
u_l_eye_upper_eyelid_closed = ud_center_l_eye_upper_eyelid_closed - (u - ud_center)

# When eyes look down, eyelids must move down accordingly

d_r_eye_lower_eyelid_open = ud_center_r_eye_lower_eyelid_open + (d - ud_center) # (With eyes looking) down: right eye lower eyelid open
d_r_eye_upper_eyelid_open = ud_center_r_eye_upper_eyelid_open + (d - ud_center)

d_r_eye_lower_eyelid_closed = ud_center_r_eye_lower_eyelid_closed + (d - ud_center)
d_r_eye_upper_eyelid_closed = ud_center_r_eye_upper_eyelid_closed + (d - ud_center)

d_l_eye_lower_eyelid_open = ud_center_l_eye_lower_eyelid_open - (d - ud_center)
d_l_eye_upper_eyelid_open = ud_center_l_eye_upper_eyelid_open - (d - ud_center)

d_l_eye_lower_eyelid_closed = ud_center_l_eye_lower_eyelid_closed - (d - ud_center)
d_l_eye_upper_eyelid_closed = ud_center_l_eye_upper_eyelid_closed - (d - ud_center)

# Eyes open and y=0

ud_center_eyes_open_l = (l, ud_center, ud_center_l_eye_upper_eyelid_open, ud_center_l_eye_lower_eyelid_open, ud_center_r_eye_upper_eyelid_open, ud_center_r_eye_lower_eyelid_open) # Left and y=0
ud_center_eyes_open_r = (r, ud_center, ud_center_l_eye_upper_eyelid_open, ud_center_l_eye_lower_eyelid_open, ud_center_r_eye_upper_eyelid_open, ud_center_r_eye_lower_eyelid_open) # Right and y=0
ud_center_eyes_open_lr_center = (lr_center, ud_center, ud_center_l_eye_upper_eyelid_open, ud_center_l_eye_lower_eyelid_open, ud_center_r_eye_upper_eyelid_open, ud_center_r_eye_lower_eyelid_open) # x=0 and y=0

# Eyes open and up

u_eyes_open_l = (l, u, u_l_eye_upper_eyelid_open, u_l_eye_lower_eyelid_open, u_r_eye_upper_eyelid_open, u_r_eye_lower_eyelid_open) # Up and left
u_eyes_open_r = (r, u, u_l_eye_upper_eyelid_open, u_l_eye_lower_eyelid_open, u_r_eye_upper_eyelid_open, u_r_eye_lower_eyelid_open) # Up and right
u_eyes_open_lr_center = (lr_center, u, u_l_eye_upper_eyelid_open, u_l_eye_lower_eyelid_open, u_r_eye_upper_eyelid_open, u_r_eye_lower_eyelid_open) # Up and x=0

# Eyes open and down

d_eyes_open_l = (l, d, d_l_eye_upper_eyelid_open, d_l_eye_lower_eyelid_open, d_r_eye_upper_eyelid_open, d_r_eye_lower_eyelid_open) # Down and left
d_eyes_open_r = (r, d, d_l_eye_upper_eyelid_open, d_l_eye_lower_eyelid_open, d_r_eye_upper_eyelid_open, d_r_eye_lower_eyelid_open) # Down and right
d_eyes_open_lr_center = (lr_center, d, d_l_eye_upper_eyelid_open, d_l_eye_lower_eyelid_open, d_r_eye_upper_eyelid_open, d_r_eye_lower_eyelid_open) # Down and x=0

# Eyes closed and y=0

ud_center_eyes_closed_l = (l, ud_center, ud_center_l_eye_upper_eyelid_closed, ud_center_l_eye_lower_eyelid_closed, ud_center_r_eye_upper_eyelid_closed, ud_center_r_eye_lower_eyelid_closed) # Left and y=0
ud_center_eyes_closed_r = (r, ud_center, ud_center_l_eye_upper_eyelid_closed, ud_center_l_eye_lower_eyelid_closed, ud_center_r_eye_upper_eyelid_closed, ud_center_r_eye_lower_eyelid_closed) # Right and y=0
ud_center_eyes_closed_lr_center = (lr_center, ud_center, ud_center_l_eye_upper_eyelid_closed, ud_center_l_eye_lower_eyelid_closed, ud_center_r_eye_upper_eyelid_closed, ud_center_r_eye_lower_eyelid_closed) # x=0 and y=0

# Eyes closed and up

u_eyes_closed_l = (l, u, u_l_eye_upper_eyelid_closed, u_l_eye_lower_eyelid_closed, u_r_eye_upper_eyelid_closed, u_r_eye_lower_eyelid_closed) # Up and left
u_eyes_closed_r = (r, u, u_l_eye_upper_eyelid_closed, u_l_eye_lower_eyelid_closed, u_r_eye_upper_eyelid_closed, u_r_eye_lower_eyelid_closed) # Up and right
u_eyes_closed_lr_center = (lr_center, u, u_l_eye_upper_eyelid_closed, u_l_eye_lower_eyelid_closed, u_r_eye_upper_eyelid_closed, u_r_eye_lower_eyelid_closed) # Up and x=0

# Eyes closed and down

d_eyes_closed_l = (l, d, d_l_eye_upper_eyelid_closed, d_l_eye_lower_eyelid_closed, d_r_eye_upper_eyelid_closed, d_r_eye_lower_eyelid_closed) # Down and left
d_eyes_closed_r = (r, d, d_l_eye_upper_eyelid_closed, d_l_eye_lower_eyelid_closed, d_r_eye_upper_eyelid_closed, d_r_eye_lower_eyelid_closed) # Down and right
d_eyes_closed_lr_center = (lr_center, d, d_l_eye_upper_eyelid_closed, d_l_eye_lower_eyelid_closed, d_r_eye_upper_eyelid_closed, d_r_eye_lower_eyelid_closed) # Down and x=0

def move_eyes(lr, ud, l_upper, l_lower, r_upper, r_lower):
    lr_servo.angle = lr
    ud_servo.angle = ud
    left_eye_upper_eyelid.angle = l_upper
    left_eye_lower_eyelid.angle = l_lower
    right_eye_upper_eyelid.angle = r_upper
    right_eye_lower_eyelid.angle = r_lower
    time.sleep(1.5)

def test_eye_movement():

    move_eyes(*ud_center_eyes_open_l)
    move_eyes(*ud_center_eyes_open_r)
    move_eyes(*ud_center_eyes_open_lr_center)

    move_eyes(*u_eyes_open_l)
    move_eyes(*u_eyes_open_r)
    move_eyes(*u_eyes_open_lr_center)

    move_eyes(*d_eyes_open_l)
    move_eyes(*d_eyes_open_r)
    move_eyes(*d_eyes_open_lr_center)

    move_eyes(*ud_center_eyes_closed_l)
    move_eyes(*ud_center_eyes_closed_r)
    move_eyes(*ud_center_eyes_closed_lr_center)

    move_eyes(*u_eyes_closed_l)
    move_eyes(*u_eyes_closed_r)
    move_eyes(*u_eyes_closed_lr_center)

    move_eyes(*d_eyes_closed_l)
    move_eyes(*d_eyes_closed_r)
    move_eyes(*d_eyes_closed_lr_center)

if __name__ == "__main__":
    try:
        test_eye_movement()
    finally:
        pca.deinit()