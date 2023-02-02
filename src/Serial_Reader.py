import serial
import matplotlib.pyplot as plt

def main():
    with serial.Serial ('COMx', 115200) as s_port:     
       s_port.write ()
       data_array.append(s_port.readline().replace(b" ", b"").strip().split(b","))
    data_array = [[b'1',b'2'], [b'4',b'5', b'6'], ['hello' ,7], [], ['h', 'j', 'k']]
    float_array = []
    float_list = []
    
    for line in data_array:
        for val in line:
            try:
                data_float = float(val)
                float_list.append(data_float)
            except ValueError:
                break
            except IndexError:
                break
        if(len(float_list) > 1):
            float_array.append(float_list) 
        float_list = []
    
    x_data = [row[0] for row in float_array]
    y_data = [row[1] for row in float_array]

    plt.plot(x_data, y_data)
    plt.suptitle('Proportional Control Response')
    plt.show()

if __name__ == "__main__":
    main()