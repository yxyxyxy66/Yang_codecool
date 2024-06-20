import socket
import select
import time
import statistics

# 超时时间，单位：秒
TIMEOUT = 0.1

# 重传次数限制
MAX_RETRIES = 2

# 发送的报文数量
NUM_PACKETS = 12

# 用于存储RTT的列表
rtts = []


def calculate_rtt(start_time, end_time):
    if end_time is not None:
        return (end_time - start_time) * 1000  # 转换为毫秒
    else:
        return None  # 如果没有接收到响应，则返回None


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.84.129', 12345)

    packets_sent = 0
    packets_received = 0
    total_rtt = 0
    start_times = []

    try:
        for i in range(NUM_PACKETS):
            message = input("请输入request消息：")
            if i==0:
                first_time=time.time()
            start_time = time.time()
            start_times.append(start_time)
            for retry in range(MAX_RETRIES + 1):
                client_socket.sendto(message.encode(), server_address)

                # 使用select来等待socket数据，直到超时
                ready = select.select([client_socket], [], [], TIMEOUT)
                if ready[0]:
                    data, address = client_socket.recvfrom(4096)
                    packets_received += 1
                    end_time = time.time()
                    rtt = calculate_rtt(start_time, end_time)
                    if rtt is not None:
                        rtts.append(rtt)
                        total_rtt += rtt
                    print(f'接收到的reply消息:{data.decode()}, ServerIP:Port:{address}, RTT:{rtt:.2f}ms')
                    break  # 成功接收，跳出重传循环
                else:
                    print('超时')
                    client_socket.sendto(message.encode(), server_address)
                    if retry >= MAX_RETRIES:
                        print('超过重传次数，放弃')
                        break  # 达到最大重传次数，放弃
            packets_sent += 1

            # 计算统计信息
        packet_loss_rate = 1 - packets_received / packets_sent
        if rtts:
            max_rtt = max(rtts)
            min_rtt = min(rtts)
            avg_rtt = total_rtt / len(rtts)
            std_dev_rtt = statistics.stdev(rtts)
        else:
            max_rtt, min_rtt, avg_rtt, std_dev_rtt = (None,) * 4

        # 打印统计信息
        print(f'Packets sent: {packets_sent}')
        print(f'Packets received: {packets_received}')
        print(f'Packet loss rate: {packet_loss_rate:.2%}')
        print(f'Max RTT: {max_rtt:.2f}ms' if max_rtt is not None else 'No RTT samples')
        print(f'Min RTT: {min_rtt:.2f}ms' if min_rtt is not None else 'No RTT samples')
        print(f'Average RTT: {avg_rtt:.2f}ms' if avg_rtt is not None else 'No RTT samples')
        print(f'RTT standard deviation: {std_dev_rtt:.2f}ms' if std_dev_rtt is not None else 'No RTT samples')
        print(f'Server overall response time (last RTT): {end_time-first_time:.2f}ms')

    finally:
        client_socket.close()


if __name__ == '__main__':
    main()