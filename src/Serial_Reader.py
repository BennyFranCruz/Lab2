import serial
import matplotlib.pyplot as plt

def main():
    with serial.Serial ('COM3', baudrate=115200) as s_port:
        #input1 = input('kp Value ')
        while (True):
            s_port.write(b'2')
            print("cycled")
        
        #x = s_port.readline()
        #print(x)
        
    #x_data = []
    #y_data = []
    
    #with serial.Serial ('COM3', 115200) as s_port:
    #    while (True):
    #        data_array = []
    #        data_array.append(s_port.readline().replace(b" ", b"").strip().split(b","))
    #        try:
    #            x_data_float = float(data_array[0])
    #            y_data_float = float(y_data_array[1])
    #            x_data.append(x_data_float)
    #            y_data.append(y_data_float)
    #        except ValueError:
    #            continue
    #        except IndexError:
    #            continue
    #        except UnicodeError: #Set this to be the error that occurs when there is no data left
    #            break
    
    #plt.plot(x_data, y_data)
    #plt.suptitle('Proportional Control Response')
    #plt.xlabel('Time')
    #plt.ylabel('Position')
    #plt.show()


if __name__ == "__main__":
    main()