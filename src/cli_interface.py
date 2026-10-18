# enhanced-task-manager-design/src/cli_interface.py
import datetime

LINE = "=" * 46
DASH = "-" * 46


class CLIInterface:
    """
    Handles all command-line interface interactions (Thai/English):
    displaying menus, taking user input, and displaying output.
    Does NOT contain business logic directly; calls methods on TaskManager.
    """
    def __init__(self, task_manager):
        self.manager = task_manager

    # ---------- display helpers ----------
    def display_menu(self):
        print("\n" + LINE)
        print("      Enhanced Task Manager (Week 11)")
        print(LINE)
        print("1. เพิ่มงานทั่วไป (Add Normal Task)")
        print("2. เพิ่มงานที่มีวันครบกำหนด (Add Due Date Task)")
        print("3. เพิ่มงานที่ระดับความสำคัญ (Add Priority Task)")
        print("4. แสดงรายการงานทั้งหมด (List All Tasks)")
        print("5. เปลี่ยนสถานะงานเป็นเสร็จสิ้น (Complete Task)")
        print("6. ลบงาน (Delete Task)")
        print("7. ค้นหางาน (Search Tasks)")
        print("8. กรองงาน (Filter Tasks)")
        print("9. เรียงลำดับงาน (Sort Tasks)")
        print("0. ออกจากโปรแกรม (Exit)")
        print(DASH)

    def show_tasks(self, title, tasks):
        if not tasks:
            print("ไม่พบงาน (No tasks found.)")
            return
        print(f"\n--- {title} ({len(tasks)} รายการ) ---")
        for task in tasks:
            print(f"- {task}")
        print(DASH)

    # ---------- input helpers (defensive) ----------
    def get_user_choice(self):
        return input("เลือกเมนู (0-9): ").strip()

    def get_task_description(self):
        while True:
            description = input("กรอกรายละเอียดงาน (Description): ").strip()
            if description:
                return description
            print("ข้อผิดพลาด: รายละเอียดงานต้องไม่เป็นค่าว่าง กรุณาลองใหม่อีกครั้ง")

    def get_due_date_input(self):
        while True:
            due_date_str = input("กรอกวันครบกำหนด (YYYY-MM-DD เช่น 2026-12-31): ").strip()
            try:
                datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                return due_date_str
            except ValueError:
                print("ข้อผิดพลาด: รูปแบบวันที่ไม่ถูกต้อง กรุณาใช้ YYYY-MM-DD (เช่น 2026-12-31)")

    def get_priority_input(self):
        while True:
            priority = input("กรอกระดับความสำคัญ (High/Medium/Low): ").strip().capitalize()
            if priority in ["High", "Medium", "Low"]:
                return priority
            print("ข้อผิดพลาด: กรุณากรอก High, Medium หรือ Low")

    def get_tags_input(self):
        tags_str = input("กรอกป้ายกำกับ (Tags คั่นด้วยจุลภาค เช่น work,urgent,home - หรือเว้นว่างได้): ").strip()
        return [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    def get_task_id(self, prompt):
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("ข้อผิดพลาด: กรุณากรอกหมายเลข ID เป็นตัวเลข")
            return None

    # ---------- main loop ----------
    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice == '1':
                description = self.get_task_description()
                tags = self.get_tags_input()
                new_task = self.manager.add_normal_task(description, tags=tags)
                print(f"[สำเร็จ]: เพิ่มงานทั่วไป ID {new_task.id} เรียบร้อยแล้ว")
            elif choice == '2':
                description = self.get_task_description()
                due_date_str = self.get_due_date_input()
                tags = self.get_tags_input()
                new_task = self.manager.add_due_date_task(description, due_date_str, tags=tags)
                print(f"[สำเร็จ]: เพิ่มงานครบกำหนด ID {new_task.id} (ครบกำหนด: {new_task.due_date:%Y-%m-%d}) เรียบร้อยแล้ว")
            elif choice == '3':
                description = self.get_task_description()
                priority = self.get_priority_input()
                tags = self.get_tags_input()
                new_task = self.manager.add_priority_task(description, priority, tags=tags)
                print(f"[สำเร็จ]: เพิ่มงานความสำคัญ ID {new_task.id} (Priority: {new_task.priority}) เรียบร้อยแล้ว")
            elif choice == '4':
                self.show_tasks("รายการงานทั้งหมด", self.manager.get_all_tasks())
            elif choice == '5':
                task_id = self.get_task_id("กรอก ID ของงานที่ต้องการเปลี่ยนเป็นเสร็จสิ้น: ")
                if task_id is not None:
                    success, message = self.manager.complete_task(task_id)
                    print(f"[{'สำเร็จ' if success else 'แจ้งเตือน'}]: {message}")
            elif choice == '6':
                task_id = self.get_task_id("กรอก ID ของงานที่ต้องการลบ: ")
                if task_id is not None:
                    success, message = self.manager.delete_task(task_id)
                    print(f"[{'สำเร็จ' if success else 'แจ้งเตือน'}]: {message}")
            elif choice == '7':
                keyword = input("กรอกคำค้นหา (ค้นใน Description และ Tags): ").strip()
                if not keyword:
                    print("ข้อผิดพลาด: คำค้นหาต้องไม่เป็นค่าว่าง")
                    continue
                self.show_tasks(f"ผลการค้นหา '{keyword}'", self.manager.search_tasks(keyword))
            elif choice == '8':
                print("เว้นว่างได้ถ้าไม่ต้องการกรองด้วยเงื่อนไขนั้น")
                status_in = input("สถานะ (completed/pending): ").strip().lower()
                status = True if status_in == "completed" else False if status_in == "pending" else None
                due_before = input("ครบกำหนดก่อนหรือในวันที่ (YYYY-MM-DD): ").strip() or None
                priority = input("ระดับความสำคัญ (High/Medium/Low): ").strip().capitalize() or None
                tag = input("ป้ายกำกับ (tag เดียว): ").strip() or None
                try:
                    result = self.manager.filter_tasks(status, due_before, priority, tag)
                    self.show_tasks("ผลการกรองงาน", result)
                except ValueError:
                    print("ข้อผิดพลาด: รูปแบบวันที่ไม่ถูกต้อง กรุณาใช้ YYYY-MM-DD")
            elif choice == '9':
                criterion = input("เรียงตาม (id, due_date, priority - ค่าเริ่มต้น: id): ").strip().lower() or "id"
                if criterion not in ("id", "due_date", "priority"):
                    print("ข้อผิดพลาด: กรุณาเลือก id, due_date หรือ priority")
                    continue
                reverse = input("เรียงย้อนกลับ (yes/no - ค่าเริ่มต้น: no): ").strip().lower() == "yes"
                self.show_tasks(f"รายการงานเรียงตาม {criterion}", self.manager.sort_tasks(criterion, reverse))
            elif choice == '0':
                print("บันทึกข้อมูลเรียบร้อย ออกจากโปรแกรม (Goodbye!)")
                break
            else:
                print("ข้อผิดพลาด: กรุณาเลือกเมนู 0-9")
