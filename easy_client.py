import socket
def start_client():
    # 创建一个UDP socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 服务器地址和端口
    server_address = ('localhost', 12345)

    try:
        while True:
            # 从用户获取消息
            message = input("请输入消息（输入'exit'退出）: ")

             # 发送数据到服务器
            client_socket.sendto(message.encode(), server_address)

            # 检查是否输入了"exit"
            if message.strip().lower() == 'exit':
                print("退出客户端")
                break

            # 接收数据
            data, server = client_socket.recvfrom(4096)

            # 打印从服务器接收到的数据
            print(f"收到来自服务器的消息: {data.decode()}")

    finally:
        # 关闭socket
        client_socket.close()
        print("客户端socket已关闭")


if __name__ == '__main__':
    start_client()

'''import socket
import select
import time

# 超时时间
TIMEOUT = 0.1

# 重传次数限制
MAX_RETRIES = 2

#发送报文次数
MAXNUM = 12

# 转换为毫秒
def calculate_rtt(start_time, end_time):
    return (end_time - start_time) * 1000

def get_server_time(data):
    # 服务器返回当前时间（字符串格式）
    return time.strftime('%H-%M-%S')

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    for num in range(MAXNUM):
        message = input("请输入request消息：")
        for retry in range(MAX_RETRIES + 1):
            start_time = time.time()
            client_socket.sendto(message.encode(), server_address)

            # 使用select来等待socket数据，直到超时
            ready = select.select([client_socket], [], [], TIMEOUT)
            if ready[0]:
                data, address = client_socket.recvfrom(4096)
                end_time = time.time()
                rtt = calculate_rtt(start_time, end_time)
                print(f'接收到的reply消息:{data.decode()}, ServerIP:Port:{address}, RTT:{rtt:.2f}ms')
                break  # 成功接收，跳出重传循环
            else:
                print('没有接收到reply，重传')
                client_socket.sendto(message.encode(), address)
                if retry >= MAX_RETRIES:
                    print('超过重传次数，放弃')
                    break  # 达到最大重传次数，放弃
    client_socket.close()

if __name__ == '__main__':
    main()'''