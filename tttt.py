
if __name__ == '__main__':
    import time
    start_time = time.time()
    tick = 1.0

    tick_count = 0
    time_since_last_update = 0
    while True:
        new_time = time.time()
        tick_count += 1
        targeted_time = start_time + tick * tick_count
        time_to_wait = targeted_time - new_time

        if time_to_wait > 0:
            time.sleep(time_to_wait)
        print("Magic happens, waited %f seconds" % time_to_wait)
