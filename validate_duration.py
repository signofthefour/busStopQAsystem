import os
from tqdm import tqdm
import argparse
import numpy as np

def get_parser():
    parser = argparse.ArgumentParser(
        description="Launch distributed process with appropriate options. ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mels_dir",
        help="Directory of preprocessed mels",
        default="/Users/mac/Downloads/vn_dataset/mels",
    )
    parser.add_argument(
        "--filelist_path",
        help="Directory of preprocessed mels",
        default="./filelist/train.txt",
    )
    return parser

def check_phoneme_duration(filepath):
    print("Checking if phoneme is equal to duration...")
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            _sen, _entry, duration, phoneme, _filename = line.split('|')
            assert len(duration.split(' ')) == len(phoneme.split(' ')), "Number of phonemes is not equal to number of duration in file: " + _filename
    print("OK")

def check_duration_mels(filelist_path, mels_dir):
    print("Checking if duration is equal to mels len...")
    with open(filelist_path, 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            _, _, duration, _, filename = line.split('|')
            total_duration = sum([int(x) for x in duration.split(' ')])
            mel = np.load(os.path.join(mels_dir, filename.replace('\n', '').replace('.wav', '.npy')))
            assert total_duration + 1 == mel.shape[1], "Mel len not equal to total duration at utterance: " + filename
    print("OK")

def main(cmd=None):
    parser = get_parser()
    args = parser.parse_args(cmd)
    if os.path.isfile(args.filelist_path):
        check_phoneme_duration(args.filelist_path)
        check_duration_mels(args.filelist_path, args.mels_dir)
            

if __name__ == "__main__":
    main()