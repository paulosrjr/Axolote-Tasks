from actions.backup_executors.scp import Scp

ka = {"hello":"1", "world":"2"}

task = Scp()
result = task.apply_async(kwargs=ka, queue="axolote", exchange="axolote", routing_key="axolote")
