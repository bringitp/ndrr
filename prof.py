import pstats
profiler = pstats.Stats("get_room_messages.prof")
profiler.strip_dirs()
profiler.sort_stats("time")
profiler.print_stats()