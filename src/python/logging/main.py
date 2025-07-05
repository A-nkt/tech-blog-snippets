import pandas as pd

from utils import logger

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"

def main():
    # input
    df = pd.read_csv(INPUT_FILE)
    logger.info('read csv : %s', INPUT_FILE)

    # process
    df['sales'] = df['price'] * df['amount']

    # output
    df.to_csv(OUTPUT_FILE, index=False)
    logger.info("output : %s", OUTPUT_FILE)


if __name__ == "__main__":
    main()