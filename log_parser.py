import csv
import re
import sys
from urllib.parse import unquote, urlparse, parse_qs
from datetime import datetime

class LogParser:
	def __init__(self, log_file, results_file):
		self.logs = self.__read_logs(log_file)
		self.results_file = results_file

	def __read_logs(self, log_file):
		with open(log_file) as raw_logs:
			raw_logs = raw_logs.readlines()

		# filter the logs to only feedback button responses and ignore my test responses
		feedback_logs = [log for log in raw_logs if "is_alert" in log and 's.molin' not in log]

		return feedback_logs

	def parse_logs(self):
		with open(self.results_file, 'w', newline='') as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			for line in self.logs:
				# regex to pull out date: (\[.*\]) and without the brackets: (?:\[)(.*)(?:\]) and select group 1
				date = re.search('(?:\[)(.*)(?:\])', line).group(1)
				datetime_utc = datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')

				# regex to pull out the URL: (\/metis\S*) returns whole url and query string but we don't have the http...com part
				url = unquote(re.search('(\/metis\S*)', line).group(0))
				query_string = urlparse(url).query

				if query_string:
					parameters = parse_qs(query_string)
					writer.writerow(['email',
									parameters['username'][0],
									datetime.strftime(datetime_utc, '%Y-%m-%d %H:%M:%S'),
									parameters['client_name'][0],
									parameters['client_id'][0],
									-1,
									-1,
									parameters['cost_center'][0],
									parameters['ranking'][0],
									parameters['country'][0],
									parameters['subregion'][0],
									re.search('\w*', parameters['region'][0]).group(0),
									'N/A',
									'N/A',
									parameters['run_date'][0],
									parameters['kpi'][0],
									parameters['is_alert'][0]])

if __name__ == '__main__':
	if len(sys.argv) == 1:
		sys.exit('Must provide the path to the log file')
	else:
		log_file = sys.argv[1]
		if len(sys.argv) > 2:
			results_file = sys.argv[2]
		else:
			results_file = 'parsed_logs.csv'

	logParser = LogParser(log_file, results_file)
	logParser.parse_logs()
