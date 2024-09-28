# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot

import json
from .Basic import Basic


class Tasks:
    def __init__(self, log, HttpRequest, Tasks, user_tasks):
        self.log = log
        self.http = HttpRequest
        self.tasks = Tasks
        self.user_tasks = user_tasks
        self.basic = Basic(log, HttpRequest)

    def start_tasks(self):
        self.log.info("📝 <y>Starting tasks ...</y>")
        if not self.tasks:
            self.log.error("🟡 <y>Tasks not found!</y>")

        for task in self.tasks:
            task_id = task["id"]
            task_type = task["type"]

            if task_type not in {"WithLink", "WithLocaleLink"}:
                continue

            self.claim_task(task_id)

        self.log.info("✅ <g>All tasks completed!</g>")

    def claim_task(self, task_id):
        if not task_id or not self.user_tasks:
            return

        for task in self.user_tasks:
            if task["id"] == task_id and task["isCompleted"]:
                return

        self.log.info(f"📝 <y>Claiming task <c>{task_id}</c> ...</y>")

        resp = self.http.post(
            url="/interlude/check-task",
            payload=json.dumps({"taskId": task_id}),
        )

        self.log.info(f"📝 <g>Task <c>{task_id}</c> claimed!</g>")
