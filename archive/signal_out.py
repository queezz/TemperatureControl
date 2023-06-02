import serial
import time
### Write down Communication program using PySerial with Micom.

port = "COM4"
baudrate = 9600

def main(): # テスト用
    with serial.Serial(port, baudrate, timeout=1) as ser:   # シリアルポートとボーレートを設定
        while True:
            print("Input Char (q:quit)", end=' > ')
            p = input()

            if p == 'q':
                break

            flag = bytes(p, 'utf-8')
            print(flag)
            ser.write(flag)   # 入力した文字を送信

        ser.close()

def main():
    with serial.Serial(port, baudrate, timeout=1) as ser:   # シリアルポートとボーレートを設定
        import random
        data = [random.randint(0,1) for i in range(100)] # ここのランダム生成列にDAQからのデータにより意味を持たせる
        for i in data:
            flag = bytes(str(i),'utf-8')
            ser.write(flag)
            time.sleep(0.01)
            print(flag)
        ser.write(bytes('0','utf-8'))
        ser.close()   

# open , main, close の三段階に分けた関数化し、全体をクラス化



if __name__ == "__main__":
    main()