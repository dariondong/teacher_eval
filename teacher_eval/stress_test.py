"""
教师评价系统 - 压力测试工具
Usage:
    python stress_test.py --url https://wed.theez.top --count 100 --concurrent 10
"""

import sys
import os
import uuid
import random
import time
import threading
from datetime import datetime

try:
    import requests
except ImportError:
    print("请先安装 requests: pip install requests")
    sys.exit(1)

GRADES = ['高一', '高二', '高三']
SUBJECTS = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '体育', '信息技术', '音乐', '美术', '心理']
OPTIONS = ['A', 'B', 'C', 'D', 'E']
Q_COUNT = 20

success = 0
failed = 0
lock = threading.Lock()
start_time = None


def build_form(device_uuid=None):
    if not device_uuid:
        device_uuid = str(uuid.uuid4())
    data = {
        'grade': random.choice(GRADES),
        'className': str(random.randint(1, 33)),
        'teacherSubject': random.choice(SUBJECTS),
        'device_uuid': device_uuid,
        'suggestions': random.choice(['', '老师很负责', '希望多互动', '讲得很好', '加油']),
    }
    for i in range(1, Q_COUNT + 1):
        data[f'q{i}'] = random.choice(OPTIONS)
    return data


def send_request(url):
    global success, failed
    try:
        data = build_form()
        r = requests.post(url, data=data, timeout=15, allow_redirects=False)
        with lock:
            if r.status_code in (200, 302):
                success += 1
            else:
                failed += 1
    except Exception as e:
        with lock:
            failed += 1


def worker(url, count):
    for _ in range(count):
        send_request(url)


def print_status(total):
    elapsed = time.time() - start_time
    rate = total / elapsed if elapsed > 0 else 0
    sys.stdout.write(
        f"\r  完成: {success + failed}/{total}  "
        f"成功: {success}  "
        f"失败: {failed}  "
        f"耗时: {elapsed:.1f}s  "
        f"速率: {rate:.1f} req/s  "
    )
    sys.stdout.flush()


def main():
    global start_time
    import argparse

    parser = argparse.ArgumentParser(description='教师评价系统压力测试')
    parser.add_argument('--url', default='https://wed.theez.top/', help='目标URL (默认: https://wed.theez.top/)')
    parser.add_argument('--count', type=int, default=100, help='总请求数 (默认: 100)')
    parser.add_argument('--concurrent', type=int, default=10, help='并发线程数 (默认: 10)')
    args = parser.parse_args()

    url = args.url.rstrip('/') + '/'
    total = args.count
    conc = args.concurrent
    per_thread = total // conc
    remainder = total % conc

    print(f"╔══ 教师评价系统压力测试 ══╗")
    print(f"  目标: {url}")
    print(f"  总请求: {total}")
    print(f"  并发: {conc}")
    print(f"  每题: {Q_COUNT} 题, 随机选择")
    print(f"╚{'═'*28}╝")
    print()

    start_time = time.time()
    threads = []

    for i in range(conc):
        c = per_thread + (1 if i < remainder else 0)
        t = threading.Thread(target=worker, args=(url, c))
        threads.append(t)
        t.start()

    # 实时进度
    try:
        while any(t.is_alive() for t in threads):
            print_status(total)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n用户中断")
        return

    for t in threads:
        t.join()

    elapsed = time.time() - start_time
    print()
    print()
    print(f"╔══ 测试结果 ══╗")
    print(f"  总请求: {total}")
    print(f"  成功:   {success}")
    print(f"  失败:   {failed}")
    print(f"  耗时:   {elapsed:.2f}s")
    print(f"  速率:   {total/elapsed:.1f} req/s" if elapsed > 0 else "  速率: N/A")
    print(f"╚{'═'*16}╝")


if __name__ == '__main__':
    main()
