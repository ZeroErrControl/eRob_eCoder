# -*- coding: utf-8 -*-
import tkinter as tk
from math import sin, cos, radians
import serial
import time
import socket


class ZeroErrEncoder:
    def __init__(self, port, baudrate=2500000, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = serial.Serial()

    def open(self):
        try:
            self.serial.port = self.port
            self.serial.baudrate = self.baudrate
            self.serial.timeout = self.timeout
            self.serial.open()
            if self.serial.isOpen():
                print("Serial port {} opened successfully, baudrate: {}".format(self.port, self.baudrate))
        except Exception as e:
            print(f"Cannot open serial port {self.port}: {e}")

    def close(self):
        if self.serial.isOpen():
            self.serial.close()
            print(f"Serial port {self.port} closed")

    def send_command(self, command):
        try:
            if self.serial.isOpen():
                self.serial.write(command)
                print(f"Command sent: {command.hex()}")
            else:
                print("Serial port not open, cannot send command")
        except Exception as e:
            print(f"Failed to send command: {e}")

    def read_data(self, expected_length):
        try:
            if self.serial.isOpen():
                data = self.serial.read(expected_length)
                if len(data) == expected_length:
                    print(f"Data received: {data.hex()}")
                    return data
                else:
                    print(f"Insufficient data received, expected {expected_length} bytes, but got {len(data)} bytes")
                    return None
            else:
                print("Serial port not open, cannot receive data")
        except Exception as e:
            print(f"Failed to receive data: {e}")
            return None


def read_encoder_angle(encoder):
    CMD_READ_ALL = bytes([0x1A])
    encoder.send_command(CMD_READ_ALL)
    time.sleep(0.01)
    response = encoder.read_data(11)
    if response:
        # Read status bytes
        status_sa = response[1]
        status_almc = response[9]
        
        # Read position and resolution data
        single_turn = response[2] | (response[3] << 8) | (response[4] << 16)
        resolution = response[5]
        multi_turn = response[6] | (response[7] << 8) | (response[8] << 16)
        
        # Check encoder status
        status_message = check_encoder_status(status_sa, status_almc)
        if status_message != "Normal active state":
            print(f"Encoder status: {status_message}")
            
        if resolution != 0:
            # Calculate single-turn angle
            single_turn_angle = (single_turn / (2**resolution)) * 360
            # Calculate total angle (including multi-turn)
            total_angle = single_turn_angle + (multi_turn * 360)
            return total_angle, single_turn_angle, status_message
    return 0, 0, "Data read failed"

def check_encoder_status(sa, almc):
    status = []
    
    if sa & 0x10:
        status.append("Single-turn startup error")
    if sa & 0x20:
        status.append("Multi-turn startup error")
    if almc & 0x04:
        status.append("Single-turn count error")
    if almc & 0x20:
        status.append("Multi-turn communication error")
    if almc & 0x40:
        status.append("Battery error")
    if almc & 0x80:
        status.append("Battery warning, voltage below 3.05V")
    
    if not status and (sa & 0xFF) == 0 and (almc & 0xFF) == 0:
        return "Normal active state"
    
    return "\n".join(status)

def update_pointer(center_x, center_y, canvas, pointer, angle):
    length = 300
    angle_adjusted = angle + 90
    end_x = center_x + length * cos(radians(angle_adjusted))
    end_y = center_y - length * sin(radians(angle_adjusted))
    base_x1 = center_x + 10 * cos(radians(angle_adjusted + 90))
    base_y1 = center_y - 10 * sin(radians(angle_adjusted + 90))
    base_x2 = center_x + 10 * cos(radians(angle_adjusted - 90))
    base_y2 = center_y - 10 * sin(radians(angle_adjusted - 90))
    canvas.coords(pointer, base_x1, base_y1, end_x, end_y, base_x2, base_y2)


def draw_scale(canvas, center_x, center_y, radius):
    outer_radius = 320
    inner_radius_major = 310
    inner_radius_minor = 330

    for i in range(360):
        angle_rad = radians(i + 90)
        outer_x = center_x + outer_radius * cos(angle_rad)
        outer_y = center_y - outer_radius * sin(angle_rad)

        if i % 10 == 0:
            inner_x = center_x + inner_radius_major * cos(angle_rad)
            inner_y = center_y - inner_radius_major * sin(angle_rad)
            if i % 30 == 0:
                text_x = center_x + (inner_radius_major - 40) * cos(angle_rad)
                text_y = center_y - (inner_radius_major - 40) * sin(angle_rad)
                canvas.create_text(text_x, text_y, text=str(i), font=("Arial", 12, "bold"))
        else:
            inner_x = center_x + inner_radius_minor * cos(angle_rad)
            inner_y = center_y - inner_radius_minor * sin(angle_rad)

        canvas.create_line(outer_x, outer_y, inner_x, inner_y, width=2)


if __name__ == "__main__":
    try:
        encoder = ZeroErrEncoder(port="/dev/ttyUSB0", baudrate=2500000, timeout=1)
        encoder.open()

        root = tk.Tk()
        root.title("eCoder")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        canvas.pack()

        center_x = screen_width // 2
        center_y = screen_height // 2
        diameter = 700
        radius = diameter // 2

        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=2)
        draw_scale(canvas, center_x, center_y, radius)

        pointer = canvas.create_polygon(center_x, center_y, center_x, center_y - radius, center_x + 10, center_y, fill="red", outline="black", width=2)
        angle_text = canvas.create_text(center_x, center_y - 200, text="0°", font=("Arial", 24, "bold"))

        # Setup Socket communication
        server_ip = "127.0.0.1"
        server_port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")

        def update_ui():
            total_angle, single_turn_angle, status = read_encoder_angle(encoder)
            
            # Display single-turn angle only
            status_text = f"{single_turn_angle:.2f}°"
            canvas.itemconfig(angle_text, text=status_text)
            
            # Update pointer position (using single-turn angle)
            update_pointer(center_x, center_y, canvas, pointer, single_turn_angle)

            # Calculate full pulse count, considering multi-turn
            full_turns = int(total_angle / 360)
            remaining_angle = total_angle % 360
            pulses = (full_turns * 524287) + int((remaining_angle / 360) * 524287)

            try:
                sock.send(f"{pulses}".encode())
            except Exception as e:
                print(f"Failed to send data: {e}")

            root.after(100, update_ui)

        root.protocol("WM_DELETE_WINDOW", lambda: (encoder.close(), sock.close(), root.destroy()))

        update_ui()
        root.mainloop()

    except KeyboardInterrupt:
        print("Program interrupted, closing resources...")
    finally:
        encoder.close()
