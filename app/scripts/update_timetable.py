# # scripts/update_timetable.py
# from utils.fetchers import fetch_timetable_html
# from utils.parsers import parse_timetable_html
# from db.connection import SessionLocal

# # Example: update timetable for a group

# def update_timetable_for_group(group_value: str):
#     html = fetch_timetable_html(group_value)
#     timetable = parse_timetable_html(html, groups=[group_value])
#     db = SessionLocal()
#     # Clear and insert new timetable data for the group
#     db.query(Timetable).filter(Timetable.group == group_value).delete()
#     for day in timetable:
#         for lesson in day:
#             db.add(Timetable(
#                 group=group_value,
#                 day=lesson.get('day', ''),
#                 lesson=lesson.get('lesson', ''),
#                 start_time=lesson.get('time', {}).get('start', ''),
#                 end_time=lesson.get('time', {}).get('end', ''),
#                 subject=lesson.get('subject', [{}])[0].get('name', ''),
#                 teacher=lesson.get('subject', [{}])[0].get('teacher', ''),
#                 room=lesson.get('subject', [{}])[0].get('room', ''),
#             ))
#     db.commit()
#     db.close()

# # Add logic to update all groups as needed
