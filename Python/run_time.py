FRAMES = 100
DATASETS = 4
N_CALLS = 100
RESOLUTIONS = 7
ENCODERS = 5
MAX_TIME_PER_FRAME = 100 #40

ms = MAX_TIME_PER_FRAME * FRAMES  * DATASETS * N_CALLS * RESOLUTIONS * ENCODERS

secs = ms/1000
hours = secs/3600
days = hours/24

print("val_set: " + str(days))


FRAMES = 1000
DATASETS = 4
N_CALLS = 40
RESOLUTIONS = 7
ENCODERS = 5
MAX_TIME_PER_FRAME = 60

ms = MAX_TIME_PER_FRAME * FRAMES  * DATASETS * N_CALLS * RESOLUTIONS * ENCODERS

secs = ms/1000
hours = secs/3600
days = hours/24

print("test_set: " + str(days))

