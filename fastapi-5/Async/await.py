# await 키워드 = I/O 대기가 발생하는 순간, 실행권을 양보하는 키워드
import asyncio
import time

# 동기방식 실행시간 -> 6초
def task_a():
    print("A 시작") # 1
    time.sleep(3)   # 2
    print("A 끝")   # 3

def task_b():
    print("B 시작") # 4
    time.sleep(3)   # 5
    print("B 끝")   # 6

# 비동기식
async def coro_a():
    print("A 시작") # 1
    await asyncio.sleep(3)  # 2 -> (양보)
    print("A 끝")   # 5

async def coro_b():
    print("B 시작") # 3
    await asyncio.sleep(3) # 4 -> (양보)
    print("B 끝")   # 6

async def main():
    a = coro_a()
    b = coro_b()
    await asyncio.gather(a, b)

print("==== 동기 실행 ====")
sync_start = time.time()
task_a()
task_b()
sync_end = time.time()
print(f"{sync_end - sync_start:.2f}초")

print("==== 비동기 실행 ====")
async_start = time.time()
asyncio.run(main())
async_end = time.time()
print(f"{async_end - async_start:.2f}초")

# [ 정리 ]
# 1. await 키워드를 통해서 코루틴 함수 안에서 실행권을 양보할 수 있다.
# 2. await 키워드는 대기가 발생하는 코드 (sleep, I/O 대기) 앞에 붙인다.
# 3. 대기시간 동안 다른 코루틴이 실행되어, 전체 프로그램 대기시간을 줄일 수 있다.

# 3초씩 대기하는 함수 100개를 실행한다면,
#   동기 방식 -> 300초
#   비동기 방식 -> 3초

# 비동기 방식의 단점
# 1. 코루틴이 정확히 어떤 순서로 실행될지 보장할 수 없음
# 2. 실행을 잘못 시키면, 오히려 더 비효율적
# -> 비동기 프로그래밍이 어떤 실행 흐름으로 동작하는지 이해하고 사용해야 함