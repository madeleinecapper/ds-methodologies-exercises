import pandas as pd

def read_log():
    with open('access.log') as f:
        lines = f.read()
        return lines
def split_content(lines):
    lines = lines.split('\n')
    return lines

def split_lines(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.split(' '))
    return new_lines

def make_frame(lines):
    for i, elmnt in enumerate(lines):
        elmnt[3:5] = [''.join(elmnt[3:5])]
        elmnt[4:7] = [''.join(elmnt[4:7])]
        if i > 8:
            elmnt[8:len(elmnt)] = [''.join(elmnt[8:len(elmnt)])]
    df =pd.DataFrame(lines, columns=['ip','dash1','dash2','timestamp','req','status','size','dash3','usr_agnt'])
    df.drop(columns=['dash1','dash2'],inplace=True)
    return df

def get_log_data():
    lines = split_lines(split_content(read_log()))
    df = make_frame(lines)
    df['timestamp'] = df.timestamp.str.replace('[', '').str.replace(']', '')
    df.timestamp = pd.to_datetime(df.timestamp.str.replace(':', ' ', 1))
    df.drop(index=13974, inplace=True)
    return df