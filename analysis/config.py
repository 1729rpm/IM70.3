"""Load config/athlete.yaml. Every analysis script gets its numbers from here, never from constants in code."""
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, 'config', 'athlete.yaml')


def load_config(path=CONFIG_PATH):
    with open(path) as f:
        return yaml.safe_load(f)


CFG = load_config()
LTHR = CFG['heart_rate']['lthr']
TREADMILL_FACTOR = CFG['data_cleaning']['treadmill_speed_factor']
DUP_OVERLAP = CFG['data_cleaning']['duplicate_overlap_fraction']
INTERVAL_WORDS = tuple(str(w).lower() for w in CFG['data_cleaning']['interval_title_words'])
GAP_DAYS = CFG['data_cleaning']['gap_days_threshold']


def is_interval_title(title):
    t = str(title or '').lower()
    return any(w in t for w in INTERVAL_WORDS)


def repo_path(*parts):
    return os.path.join(ROOT, *parts)
