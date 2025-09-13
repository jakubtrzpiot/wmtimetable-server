def parse_courses(html: str) -> list[dict[str, str]]:
    """
    Parse the course list HTML and return a list of dicts with label and value.
    """
    soup = BeautifulSoup(html, 'html.parser')
    courses = []
    for a in soup.select('#oddzialy a[href^="plany/o"]'):
        label = a.get_text(strip=True)
        href = a.get('href', '')
        value = ''.join(filter(str.isdigit, href))
        courses.append({'label': label, 'value': value})
    return courses

# Python port of timetable parser logic
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# Import fetch and parse functions from new modules
from .fetchers import fetch_courses_html
from .parsers import parse_courses
from .helpers import transpose, strip_null_values_from_edges


def unwrap(node) -> List[Dict[str, Any]]:
    # node: BeautifulSoup Tag
    # Returns a list of subject dicts
    subjects = []
    p_tags = node.find_all(class_='p')
    n_tags = node.find_all(class_='n')
    s_tags = node.find_all(class_='s')
    for index, subject in enumerate(p_tags):
        p = subject.get_text().replace('  ', ' ')
        if p.split(' ')[0].strip().startswith('#'):
            continue
        if p[:2] == 'J ':
            name = ' '.join(p.split(' ')[:2]).strip().split('-')[0]
        else:
            name = ' '.join(p.split(' ')[:-1]).strip()
        # week
        try:
            week = p.split(' ')[-1].split('-')[1].strip().replace('(', '').replace(')', '').replace('.', '').lower()[0]
        except Exception:
            try:
                week = subject.next_sibling.strip().replace('(', '').replace(')', '').replace('-', '').replace('.', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').lower()
            except Exception:
                week = ''
        # teacher
        try:
            teacher = n_tags[index].get_text().upper()
        except Exception:
            try:
                teacher = subject.next_sibling.next_sibling.get_text()[1:].replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').upper()
            except Exception:
                teacher = ''
        t = p[:2] == 'J ' and 'j' or p.strip().split(' ')[-1].split('-')[0].lower()
        type_ = t[0] if t else ''
        if len(t) > 1:
            group = t
        elif type_ == 'j':
            try:
                group = subject.next_sibling.next_sibling.get_text().replace('#', '').lower()
            except Exception:
                group = ''
        elif type_ in ['ć', 'w']:
            group = 'all'
        else:
            group = None
        try:
            room = s_tags[index].get_text().split('-')[:-1]
            room = '-'.join(room) if room else s_tags[index].get_text()
            room = room.split('/')[0].strip()
            if room.lower() == 'e-learning':
                room = 'ONLINE'
        except Exception:
            room = ''
        # FIXME: remove this, temporarily disable teachers initials
        teacher = group if type_ == 'j' else ''
        subjects.append({
            'name': name,
            'type': type_,
            'group': group,
            'week': week,
            'teacher': teacher,
            'room': room,
        })
    return subjects


# The main parse_timetable function will need to be adapted to your actual HTML and fetching logic.
# This is a placeholder for integration with FastAPI and your backend fetch logic.

def parse_timetable_html(html: str) -> List[List[Dict[str, Any]]]:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(class_='tabela')
    if not table:
        return []
    rows = table.find_all('tr')
    # skip header row
    matrix = [row.find_all(['td', 'th']) for row in rows[1:]]
    # transpose and skip hour column
    transposed = transpose(matrix)[1:]
    # get hours
    hours = []
    for hour_cell in transposed[0]:
        hour_text = hour_cell.get_text().replace(' ', '').split('-')
        if len(hour_text) == 2:
            hours.append({'start': hour_text[0], 'end': hour_text[1]})
        else:
            hours.append({'start': '', 'end': ''})
    timetable = []
    for day in transposed[1:]:
        lessons = []
        for i, lesson_cell in enumerate(day):
            time = hours[i] if i < len(hours) else {'start': '', 'end': ''}
            lessons.append({
                'time': time,
                'subject': unwrap(lesson_cell) or [],
            })
        timetable.append(lessons)

    return timetable

def parse_groups(html: str) -> list[dict[str, str]]:
    """
    Parse the course list HTML and return a list of dicts with label and value.
    """
    soup = BeautifulSoup(html, 'html.parser')
    courses = []
    for a in soup.select('#oddzialy a[href^="plany/o"]'):
        label = a.get_text(strip=True)
        href = a.get('href', '')
        value = ''.join(filter(str.isdigit, href))
        courses.append({'label': label, 'value': value})
    return courses




# Course parsing functions would be implemented similarly, using BeautifulSoup to extract course names and values from HTML.



# const transpose = (array: Array<any>) => {
#   return array[0].map((_: any, i: number) => {
#     return array.map(col => {
#       return col[i];
#     });
#   });
# };

# const unwrap = (node: any) => {
#   if (node.childNodes.length > 1 || node.firstChild.childNodes) {
#     //one or more subjects
#     return Array.from(node.getElementsByAttribute('class', 'p'))
#       .filter(
#         (subject: any) =>
#           subject.firstChild.nodeValue.split(' ')[0].trim()[0] !== '#',
#       )
#       .map((subject: any, index: number) => {
#         const p = subject.firstChild.nodeValue.replace(/  +/g, ' ');
#         const name =
#           p.substr(0, 2) === 'J '
#             ? p.split(' ').slice(0, 2).join(' ').trim().split('-')[0]
#             : p.split(' ').slice(0, -1).join(' ').trim();

#         let week, teacher;
#         try {
#           week = p
#             .split(' ')
#             [p.split(' ').length - 1].split('-')[1]
#             .trim()
#             .replace(/[()]/g, '')
#             .replace('.', '')
#             .toLowerCase()[0];
#         } catch (err) {
#           week = subject.nextSibling.nodeValue
#             .trim()
#             .replace(/[()\-0-9]/g, '')
#             .replace('.', '')
#             .toLowerCase();
#         }

#         try {
#           teacher = node
#             .getElementsByAttribute('class', 'n')
#             [index].firstChild.nodeValue.toUpperCase();
#         } catch (err) {
#           teacher = subject.nextSibling.nextSibling.firstChild.nodeValue
#             .slice(1)
#             .replace(/[0-9]/g, '')
#             .toUpperCase();
#         }

#         const t =
#           p.substr(0, 2) === 'J '
#             ? 'j'
#             : p
#                 .trim()
#                 .split(' ')
#                 [p.split(' ').length - 1].split('-')[0]
#                 .toLowerCase();

#         let type = t[0];

#         const group =
#           t.length > 1
#             ? t
#             : type === 'j'
#             ? subject.nextSibling.nextSibling.firstChild.nodeValue
#                 .replace('#', '')
#                 .toLowerCase()
#             : ['ć', 'w'].includes(type)
#             ? 'all'
#             : null;

#         let room = node
#           .getElementsByAttribute('class', 's')
#           [index].firstChild.nodeValue.split('-')
#           .slice(0, -1)
#           .join('-')
#           .split('/')[0]
#           .trim();
#         room.toLowerCase() === 'e-learning' ? (room = 'ONLINE') : null;

#         //FIXME: remove this, temporarily disable teachers initals
#         teacher = type == 'j' ? group : '';

#         return {
#           name,
#           type,
#           group,
#           week,
#           teacher,
#           room,
#         } as Subject;
#       });
#   } else {
#     //no subject
#     return [];
#   }
# };

# const stripNullValuesFromEdges = (array: Array<any>) => {
#   // Remove null values from the beginning of the array
#   while (array.length > 0 && array[0].subject === null) {
#     array.shift();
#   }

#   // Remove null values from the end of the array
#   while (array.length > 0 && array[array.length - 1].subject === null) {
#     array.pop();
#   }

#   return array;
# };

# const filter = (timetable: Day[], groups: Array<string>): Timetable => {
#   // console.log('timetable:', timetable, '\ngroups:', groups);
#   const byWeek = (week: string): Day[] =>
#     timetable.map(
#       day =>
#         day &&
#         stripNullValuesFromEdges(
#           day.map(({time, subject}: Period) => ({
#             time,
#             subject:
#               (subject as Subject[])?.filter(subject => {
#                 if (subject.week.includes(week)) {
#                   if (groups.includes('en0') && subject.type == 'j')
#                     return true;
#                   if (groups.includes(subject.group)) return true;
#                 }
#               })[0] || null,
#           })),
#         ),
#     );

#   const result = {n: byWeek('n'), p: byWeek('p')}
#   // console.log('Filter result', result);
#   return result;
# };

# export const parseTimetable = async (course: number): Promise<Timetable> => {
#   const groups = await asyncStorage.getItem('groups');
#   // const do_compact = await asyncStorage.getItem('compact');
#   // const compact = (timetable: Timetable): Timetable => {
#   //   return timetable.map(day => {
#   //     const compacted: Period[] = [];
#   //     let i = 0;
#   //     while (i < day.length) {
#   //       const lesson = day[i];
#   //       if (lesson.subject) {
#   //         let j = i + 1;
#   //         while (
#   //           j < day.length &&
#   //           //@ts-expect-error
#   //           day[j]?.subject?.name === lesson.subject.name &&
#   //           //@ts-expect-error
#   //           day[j]?.subject?.type === lesson.subject.type &&
#   //           j - i < 3
#   //         ) {
#   //           j++;
#   //         }
#   //         compacted.push({
#   //           time: {
#   //             start: lesson.time.start,
#   //             end: day[j - 1].time.end,
#   //           },
#   //           subject: lesson.subject,
#   //         });
#   //         i = j;
#   //       } else {
#   //         compacted.push(lesson);
#   //         i++;
#   //       }
#   //     }
#   //     return compacted.filter(lesson => lesson.subject);
#   //   });
#   // };

#   // const res = true ? compact(timetable) : timetable; // do_compact
#   return await fetch(`${WM_URL}/plany/o${course}.html`)
#     .then(res => {
#       if (!res.ok) {
#         throw new Error('Network response was not ok.');
#       }
#       return res.text();
#     })
#     .then(html => {
#       const doc = new parser().parseFromString(
#         html.replace(/(\r\n|\n|\r)/gm, ''),
#         'text/html',
#       );

#       const transposed = transpose(
#         Array.from(
#           doc.getElementsByAttribute('class', 'tabela')[0].childNodes,
#           (row: any) => Array.from(row.childNodes),
#         ).slice(1),
#       ).slice(1);

#       const hours = transposed[0].map((hour: any) => {
#         hour = hour.firstChild.data.replace(/(\s)/gm, '').split('-');
#         return {start: hour[0], end: hour[1]};
#       });

#       let timetable = transposed.slice(1).map((day: any) => {
#         return day.map((lesson: any, i: number) => {
#           const time = hours[i];
#           return {
#             time,
#             subject: unwrap(lesson) || [],
#           };
#         });
#       });

#       // type PeriodProps = {
#       //   dayIndex: number;
#       //   lessonIndex: number | number[];
#       //   subject: {
#       //     name: string;
#       //     group?: string;
#       //     week?: string;
#       //     type?: string;
#       //     teacher?: string;
#       //     room?: string;
#       //   };
#       // }

#       // const insertPeriods = ({lessonIndex, dayIndex, subject}: PeriodProps) => {
#       //   for (let idx of lessonIndex as number[]) {
#       //     timetable[dayIndex][idx].subject.push(subject);
#       //   }
#       // };
#       // const deletePeriods = ({lessonIndex, dayIndex, subject}: PeriodProps) => {
#       //   for (let idx of lessonIndex as number[]) {
#       //     let subjectIndex = 0;
#       //     while (subjectIndex > -1) {
#       //       subjectIndex = timetable[dayIndex][idx].subject
#       //         .slice(subjectIndex)
#       //         .findIndex((s: Subject) => s.name === subject.name);

#       //       timetable[dayIndex][idx].subject.pop(subjectIndex);
#       //     }
#       //   }
#       // };

#       timetable = filter(timetable, groups);
#       // console.log(res);
#       return timetable
#     })
#     .catch(err => err && console.error(err, 'parseTimetable'));
# };


# # Python version of getGroups (parseGroups) for extracting group names and values from HTML
# import re
# from bs4 import BeautifulSoup
# from typing import Dict

# // export const parseCourseName = async (course: number): Promise<courseProps> => {
# //   return await fetch(`${WM_URL}/plany/o${course}.html`)
# //     .then(res => {
# //       if (!res.ok) {
# //         throw new Error('Network response was not ok.');
# //       }
# //       return res.text();
# //     })
# //     .then(html => {
# //       const doc = new parser().parseFromString(
# //         html.replace(/(\r\n|\n|\r)/gm, ''),
# //         'text/html',
# //       );

# //       return {
# //         label: doc.getElementsByAttribute('class', 'tytulnapis')[0].firstChild
# //           .nodeValue,
# //         value: course,
# //       };
# //     });
# // };