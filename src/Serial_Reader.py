import serial
import matplotlib.pyplot as plt
import time

def main():
    with serial.Serial ('COM6', baudrate=115200, timeout=1000) as s_port:
        print(s_port)
        input1 = input('kp Value ')
        input1 = bytes(input1, 'utf-8')
        s_port.write(input1)
        
    x_data = []
    y_data = []
    
    with serial.Serial ('COM6', 115200) as s_port:
        while (True):
            data_array = []
            data = s_port.readline()
            data_array.append(data.strip().split(b","))
            if data_array[0][0] == b'end':#if its blank break out of the while loop
                break
            try:
                x_data_float = float(data_array[0][0])
                y_data_float = float(data_array[0][1])
                x_data.append(x_data_float)
                y_data.append(y_data_float)
            except ValueError:
                continue
            except IndexError:
                continue
            except UnicodeError: #Set this to be the error that occurs when there is no data left
                break
    
    plt.plot(x_data, y_data)
    plt.suptitle('Slow Settling Response')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.show()


if __name__ == "__main__":
    main()