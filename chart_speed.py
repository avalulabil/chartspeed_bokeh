import pandas as pd
import re
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

def extract_data_from_line(line, pattern):
    
    match = re.search(pattern, line)
    return match.group(1) if match else None

def parse_file(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {
        "Timestamp": [],
        "Bitrate": [],
        "Interval": []
    }

    current_timestamp = None
    timestamp_pattern = r"Timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    interval_pattern = r"(\d+\.\d+-\d+\.\d+)\s+sec"
    bitrate_pattern = r"(\d+\.\d+)\s+Mbits/sec"

    for line in lines:
        if "Timestamp:" in line:
            current_timestamp = extract_data_from_line(line, timestamp_pattern)
        elif re.match(r"\[\s*\d+\]", line):
            interval = extract_data_from_line(line, interval_pattern)
            bitrate = extract_data_from_line(line, bitrate_pattern)

            if interval and bitrate:
                data["Timestamp"].append(current_timestamp)
                data["Bitrate"].append(float(bitrate))
                data["Interval"].append(interval)

    return pd.DataFrame(data)

def plot_network_speed(df):

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    source = ColumnDataSource(df)

    p = figure(title="Network Speed Chart", 
               x_axis_label='Time', 
               y_axis_label='Bitrate (Mbits/sec)',
               x_axis_type='datetime')

    p.line('Timestamp', 'Bitrate', source=source, legend_label="Bitrate", line_width=2)

    hover = HoverTool(tooltips=[("Bitrate", "@Bitrate Mbits/sec"), ("Interval", "@Interval")])
    p.add_tools(hover)

    output_file("line_chart.html")
    show(p)

# Main execution
file_path = 'soal_chart_bokeh.txt'
df = parse_file(file_path)
plot_network_speed(df)
