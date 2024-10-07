import subprocess
import sys
import os
import csv


if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    print('Usage: {} <csv_file> <custom yt-dlp options>'.format(sys.argv[0]))
    exit(1)

with open(sys.argv[1], 'r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        url = row[0]
        target_path = os.path.dirname(row[1])
        output_template = os.path.basename(row[1]) + '.%(ext)s'
        custom_args = sys.argv[2:] if len(sys.argv) > 2 else []
        yt_dlp_cmd = ([
                       'poetry',
                       'run',
                       'yt-dlp',
                       '-P', target_path,
                       '-o', output_template,
                      ] +
                       custom_args +
                       [url])
        print('\n\n#### Executing {}'.format(' '.join(yt_dlp_cmd)))
        subprocess.run(yt_dlp_cmd)
