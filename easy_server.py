import socket
def start_server():
    # 创建一个UDP socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定到本地地址和端口
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    print(f"服务器正在监听 {server_address[0]}:{server_address[1]}")

    while True:
        # 接收数据
        data, address = server_socket.recvfrom(4096)

        # 检查是否接收到"exit"
        if data.decode().strip().lower() == 'exit':
            print("收到退出请求，关闭服务器")
            break

            # 发送数据回客户端
        print(f"收到来自 {address} 的消息: {data.decode()}")
        server_socket.sendto(data, address)

        # 关闭socket
    server_socket.close()


if __name__ == '__main__':
    start_server()