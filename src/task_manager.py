# enhanced-task-manager-design/src/task_manager.py
# No direct file I/O here, uses DataPersistence.
import datetime
from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence


class TaskManager:
    """
    Manages the collection of various Task objects.
    Focuses on business logic: add, list, complete, delete, search, filter, sort.
    """
    def __init__(self, data_file='data/tasks.json'):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        """Generates the next unique ID for a new task."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def _save_changes(self):
        """Internal helper to save tasks via the persistence layer."""
        self.persistence.save_tasks(self.tasks)

    # --- Basic CRUD Operations (already existing, but now using new persistence) ---
    def add_normal_task(self, description, tags=None):
        new_task = Task(self.next_id, description, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task  # Return task for CLI confirmation

    def add_due_date_task(self, description, due_date_str, tags=None):
        new_task = DueDateTask(self.next_id, description, due_date_str, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def add_priority_task(self, description, priority, tags=None):
        new_task = PriorityTask(self.next_id, description, priority, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def get_task_by_id(self, task_id):
        """Helper to find a task by ID."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            if not task.completed:
                task.mark_complete()
                self._save_changes()
                return True, "Task marked as completed."
            else:
                return False, "Task is already completed."
        return False, "Task not found."

    def delete_task(self, task_id):
        original_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < original_len:
            self._save_changes()
            return True, "Task deleted successfully."
        return False, "Task not found."

    # --- New/Enhanced Features (implemented from PLAN.md) ---
    def get_all_tasks(self):
        """Returns all tasks. Useful for listing."""
        return list(self.tasks)

    def search_tasks(self, keyword):
        """Searches tasks by keyword in description or tags (case-insensitive)."""
        kw = keyword.lower()
        return [task for task in self.tasks
                if kw in task.description.lower() or any(kw in tag.lower() for tag in task.tags)]

    def filter_tasks(self, status=None, due_date_before=None, priority=None, tag=None):
        """
        Filters tasks by any combination of:
          status (True=completed / False=pending), due_date_before (YYYY-MM-DD),
          priority (High/Medium/Low), tag (single tag).
        """
        filtered = list(self.tasks)
        if status is not None:
            filtered = [t for t in filtered if t.completed == status]
        if due_date_before:
            limit = datetime.datetime.strptime(due_date_before, '%Y-%m-%d').date()
            filtered = [t for t in filtered if isinstance(t, DueDateTask) and t.due_date <= limit]
        if priority:
            filtered = [t for t in filtered if isinstance(t, PriorityTask) and t.priority == priority]
        if tag:
            filtered = [t for t in filtered if tag.lower() in (x.lower() for x in t.tags)]
        return filtered

    def sort_tasks(self, criterion="id", reverse=False):
        """
        Sorts tasks by 'id', 'due_date' or 'priority'.
        Tasks without the field (e.g. a normal task when sorting by due date) go last.
        """
        if criterion == "due_date":
            dated = sorted([t for t in self.tasks if isinstance(t, DueDateTask)], key=lambda t: t.due_date, reverse=reverse)
            return dated + [t for t in self.tasks if not isinstance(t, DueDateTask)]
        if criterion == "priority":
            order = {"High": 1, "Medium": 2, "Low": 3}
            ranked = sorted([t for t in self.tasks if isinstance(t, PriorityTask)],
                            key=lambda t: order.get(t.priority, 99), reverse=reverse)
            return ranked + [t for t in self.tasks if not isinstance(t, PriorityTask)]
        return sorted(self.tasks, key=lambda t: t.id, reverse=reverse)
