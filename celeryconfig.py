import os

broker_url = f"redis://{os.getenv('REDIS_HOST','localhost')}:6379/0"
result_backend = f"redis://{os.getenv('REDIS_HOST','localhost')}:6379/1"
worker_prefetch_multiplier = 1
task_acks_late = True
worker_max_tasks_per_child = 100
# Retry settings
task_annotations = {'*': {'max_retries': 3, 'default_retry_delay': 30}}
