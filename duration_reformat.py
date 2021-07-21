import argparse
import os
from collections import namedtuple
from tqdm import tqdm
import librosa

def get_parser():
    parser = argparse.ArgumentParser(
        description="Launch distributed process with appropriate options. ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--textgrid_dir",
        help="The path of textgrid format",
        default="mfa/",
    )
    parser.add_argument(
        "--filelist_path",
        help="path to standard input of adaspeech",
        default='filelist/train.txt'
    )
    return parser


Entry = namedtuple("Entry", ["start",
                             "stop",
                             "name",
                             "tier"])

def read_textgrid(filename):
    """
    Reads a TextGrid file into a dictionary object
    each dictionary has the following keys:
    "start"
    "stop"
    "name"
    "tier"
    Points and intervals use the same format, 
    but the value for "start" and "stop" are the same
    """
    if isinstance(filename, str):
        with open(filename, "r") as f:
            content = _read(f)
    elif hasattr(filename, "readlines"):
        content = _read(filename)
    else:
        raise TypeError("filename must be a string or a readable buffer")

    interval_lines = [i for i, line in enumerate(content)
                      if line.startswith("intervals [")
                      or line.startswith("points [")]
    tier_lines = []
    tiers = []
    for i, line in enumerate(content):
        if line.startswith("name ="):
            tier_lines.append(i)
            tiers.append(line.split('"')[-2]) 

    interval_tiers =  _find_tiers(interval_lines, tier_lines, tiers)
    assert len(interval_lines) == len(interval_tiers)
    return [_build_entry(i, content, t) for i, t in zip(interval_lines, interval_tiers)]

def _build_entry(i, content, tier):
    """
    takes the ith line that begin an interval and returns
    a dictionary of values
    """
    start = _get_float_val(content[i + 1])  # addition is cheap typechecking
    if content[i].startswith("intervals ["):
        offset = 1
    else:
        offset = 0 # for "point" objects
    stop = _get_float_val(content[i + 1 + offset])
    label = _get_str_val(content[i + 2 + offset])
    return Entry(start=start, stop=stop, name=label, tier=tier)


def _get_float_val(string):
    """
    returns the last word in a string as a float
    """
    return float(string.split()[-1])


def _get_str_val(string):
    """
    returns the last item in quotes from a string
    """
    return string.split('"')[-2]


def _find_tiers(interval_lines, tier_lines, tiers):
    tier_pairs = zip(tier_lines, tiers)
    cur_tline, cur_tier = next(tier_pairs) 
    next_tline, next_tier = next(tier_pairs, (None, None))
    tiers = []
    for il in interval_lines:
        if next_tline is not None and il > next_tline:
            cur_tline, cur_tier = next_tline, next_tier
            next_tline, next_tier = next(tier_pairs, (None, None))           
        tiers.append(cur_tier)
    return tiers 


def _read(f):
    return [x.strip() for x in f.readlines()]

def write_csv(textgrid_list, wavfile_name, filename=None, sep="|", window_len=1024, hop_size=256, sample_rate=22050, header=False, save_gaps=False, meta=False):
    """
    Writes a list of textgrid dictionaries to a csv file.
    If no filename is specified, csv is printed to standard out.
    """
    columns = list(Entry._fields)
    if filename:
        f = open(filename, 'a')
    if header:
        hline = sep.join(columns)
        if filename:
            f.write(hline + "\n")
        else:
            print(hline)
    sentence = ""
    entry_frame = []
    duration = []
    phoneme = ""
    for entry in textgrid_list:  # not skip unlabeled intervals
        if entry.tier == 'words':
            sentence += ' ' + (entry.name if entry.name != '' else '-') + ' '
        else:
            phoneme +=  ' ' + (entry.name if entry.name != '' else '-') + ' '
            entry_frame.append(int(entry.start * sample_rate / hop_size))
    entry_frame.append(int(textgrid_list[-1].stop * sample_rate / hop_size))
    sentence = sentence[1:-1]
    phoneme = phoneme[1:-1]
    duration = list(map(lambda x, y: x - y, entry_frame[1:], entry_frame[0: -1]))
    if filename:
        f.write('|'.join([sentence, 
                            ' '.join([str(n) for n in entry_frame]),
                            ' '.join([str(n) for n in duration]), phoneme, wavfile_name[6:]]))
        f.write('\n')
    else:
        print(sentence)
    if filename:
        f.flush()
        f.close()
    if meta:
        with open(filename + ".meta", "w") as metaf:
            metaf.write("""---\nunits: s\ndatatype: 1002\n""")

def main(cmd=None):
    parser = get_parser()
    args = parser.parse_args(cmd)
    if os.path.isfile(args.filelist_path):
        with open(os.path.join(os.getcwd(), args.filelist_path), "w") as f:
            f.write("")
    for filename in tqdm(os.listdir(os.path.join(os.getcwd(), args.textgrid_dir))):
        tgrid = read_textgrid(os.path.join(os.getcwd(), args.textgrid_dir, filename))
        wavfile_name = filename.split('/')[-1][:-9] + '.wav'
        write_csv(tgrid, wavfile_name, os.path.join(os.getcwd(), args.filelist_path))

if __name__ == "__main__":
    main()