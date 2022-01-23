import time
import logging


def main():
    slow_job(1)
    slow_job(2)
    slow_job(3)


def slow_job(n):
    """
    引数で指定した秒数だけ時間のかかる処理を行う関数。
    time.sleep()を使って擬似的に時間がかかるようにしている。
    """
    logging.info(f'Job {n} will take {n} seconds')
    time.sleep(n)  # n秒待つ。
    logging.info(f'Job {n} finished')

if __name__ == '__main__':
    # INFOレベル以上のログを出力し、ログに時刻を含める。
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    main()
