# Log Parser
Script to parse logs of HTTP requests into data of specific columns for a database.

## Logs
Request are of the form:
```10.255.0.2 - - [07/Feb/2018:13:07:09 +0000] "GET <page>.html?<query_string> HTTP/1.1" 200 1196 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" "-"
```

## Usage
To parse logs:
```python log_parser.py <log file> [OPTIONAL: <results file>]
```
