import socket
import random

# 丢包率
PACKET_LOSS_RATE = 0.1
# 发送的报文数量
NUM_PACKETS = 12

def main():
    # 创建一个UDP socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定到本地地址和端口
    server_address = ('192.168.84.129', 12345)
    server_socket.bind(server_address)

    print(f"服务器正在监听 {server_address[0]}:{server_address[1]}")

    while True:
        data, address = server_socket.recvfrom(4096)
        print(f'接收到的信息 {data.decode()} from {address}')
        # 随机是否发送响应
        if random.random() > PACKET_LOSS_RATE:
            print('发送reply')
            server_socket.sendto(data, address)
        else:
            print('丢包')

if __name__ == '__main__':
    main()