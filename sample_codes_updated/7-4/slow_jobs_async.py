import asyncio
import logging


def main():
    # 3つのコルーチンを作成。コルーチンはこの時点では実行されない。
    coroutines = [slow_job(1), slow_job(2), slow_job(3)]
    # イベントループで3つのコルーチンを並行実行し、3つとも終了するまで待つ。
    asyncio.run(asyncio.wait(coroutines))


async def slow_job(n: int):
    """
    引数で指定した秒数だけ時間のかかる処理を非同期で行うコルーチン。
    asyncio.sleep()を使って擬似的に時間がかかるようにしている。
    """
    logging.info(f'Job {n} will take {n} seconds')
    await asyncio.sleep(n)  # n秒sleepする処理が終わるまで待つ。
    logging.info(f'Job {n} finished')

if __name__ == '__main__':
    # INFOレベル以上のログを出力し、ログに時刻を含める。
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    main()
