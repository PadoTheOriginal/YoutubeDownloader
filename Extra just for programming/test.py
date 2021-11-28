if __name__ == "__main__":
    from time import time
    from statistics import mean

    while True:
        Input = input("INPUT:")
        times = []
        def func():
            for i in range(10000):
                pass

        for _ in range(1, 10001):
            start = time()
            #Test the speed of something
            func()
            end = time()
            times.append(end - start)

        print(mean(times))