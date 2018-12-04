import collections
import re
from datetime import datetime

def get_datetime(record):
  return datetime.strptime(record, '%Y-%m-%d %H:%M')

def init_guard_object(record):
  return {
    'shift_starts': [record['datetime']],
    'wakes': [],
    'falls': []
  }

def get_guard_activity(records):
  guards = {}
  current_guard_id = 0
  for r in records:
    guard_id = r['guard_id']
    if guard_id:
      current_guard_id = guard_id
      if guard_id in guards:
        guards[guard_id]['shift_starts'].append(r['datetime'])
      else:
        guards[guard_id] = init_guard_object(r)
      continue

    if r['wakes']:
      guards[current_guard_id]['wakes'].append(r['datetime'])
    
    if r['falls']:
      guards[current_guard_id]['falls'].append(r['datetime'])
    
  return guards

def get_guard_id(record_text):
  try:
    return int(re.search('#(\d+)', record_text).group(1))
  except:
    return None

def parse_record(record):
  result = re.search('\[(.+)\](.+)', record)
  datetime = get_datetime(result.group(1))
  text = result.group(2)
  return {
    'datetime': datetime,
    'text': text,
    'guard_id': get_guard_id(text),
    'wakes': 'wakes' in text,
    'falls': 'falls' in text
  }

def sort_records(records):
  parsed = [parse_record(r) for r in records]
  return sorted(parsed, key=lambda x: x['datetime'])

def get_laziest_guard(guard_activity):
  max_time_asleep = 0
  max_guard_id = 0
  most_common_minute = 0

  for (guard_id, activity) in guard_activity.items():
    time_asleep = 0
    minutes_asleep = []
    for index, dt in enumerate(activity['wakes']):
      waking_minute = dt.minute
      falling_minute = activity['falls'][index].minute
      asleep_minutes_this_period = list(range(falling_minute, waking_minute))
      time_asleep += len(asleep_minutes_this_period)
      minutes_asleep += asleep_minutes_this_period
    minute_counts = collections.Counter(minutes_asleep)
    activity['minutes'] = minute_counts
    if time_asleep > max_time_asleep:
      max_time_asleep = time_asleep
      max_guard_id = guard_id
      most_common_minute = minute_counts.most_common(1)
  return (max_guard_id, most_common_minute)

def main():
  records = [x.rstrip() for x in open('input.txt', 'r').readlines()]
  sorted_records = sort_records(records)
  guard_activity = get_guard_activity(sorted_records)
  laziest_guard = get_laziest_guard(guard_activity)
  result = int(laziest_guard[0]) * int(laziest_guard[1][0][0])
  print(result)

  mcm_actual = (0, 0)
  g_id = 0
  for (guard_id, activity) in guard_activity.items():
    mcm = activity['minutes'].most_common(1)
    activity['mcm'] = mcm
    print(mcm)
    if mcm == []:
      continue
    if mcm[0][1] > mcm_actual[1]:
      mcm_actual = mcm[0]
      g_id = guard_id

  print(mcm_actual, g_id) 
  

if __name__ == '__main__':
  main()
