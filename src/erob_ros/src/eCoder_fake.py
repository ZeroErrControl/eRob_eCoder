import socket
import time
import select
import sys

def angle_to_pulses(angle):
    # Convert angle to pulses (524287 pulses per 360 degrees)
    full_turns = int(angle / 360)
    remaining_angle = angle % 360
    pulses = (full_turns * 524287) + int((remaining_angle / 360) * 524287)
    return pulses

def main():
    # Setup Socket communication
    server_ip = "127.0.0.1"
    server_port = 8080
    
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        
        # Initial angle input
        print("Enter angle: ", end='', flush=True)
        angle = float(input())
        pulses = angle_to_pulses(angle)
        
        while True:
            # Check if there's input available
            if select.select([sys.stdin], [], [], 0.0)[0]:
                try:
                    print("Enter angle: ", end='', flush=True)
                    angle = float(input())
                    pulses = angle_to_pulses(angle)
                except ValueError:
                    print("Please enter a valid number")
                    continue
            
            try:
                # Send pulses through socket continuously
                sock.send(f"{pulses}".encode())
                time.sleep(0.1)  # Add a small delay
                
            except Exception as e:
                print(f"Error: {e}")
                break
                
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()