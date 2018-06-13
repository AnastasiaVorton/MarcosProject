import os
import re

from evaluation import *
from multipleworld import *
from midi_reader import read_all_dataset

instrument_outputs = {0: 12, 1: 24, 25: 36, 33: 24}


def main() -> None:
    # Config and data initialization

    instruments = read_settings()
    config = create_config(instruments)
    data = read_all_dataset(1)
    training_set = random.sample(data, 5)

    # Multiple world initialization
    # p = Checkpointer.restore_checkpoint('checkpoint-4')
    p = Multipleworld(config, instruments)
    p.add_reporter(StdOutReporter(True))
    p.add_reporter(StatisticsReporter())
    p.add_reporter(Checkpointer(instruments=instruments, generation_interval=1, filename_prefix='checkpoint-'))

    # Running and result handling
    evaluator = Evaluator(training_set)
    winner = p.run(evaluator.evaluate_genomes, 100)
    print(winner)


def read_settings() -> Dict[int, int]:
    """
    Reads the instrument list from the standard input
    :return: a map with requested instruments and numbers of outputs for each instrument
    """
    instruments_input = input("Please enter the instruments' ids as a comma-separated list (e.g.: 1, 33) [1]: ")
    if instruments_input == '':
        instruments_input = '1'
    instruments = {int(i) for i in re.split('[^0-9]+', instruments_input)}
    return {i: instrument_outputs[i] for i in instruments}


def create_config(instruments: Dict[int, int]) -> Config:
    """
    Sets ANN's parameters based on the number of octaves and instruments the user wants to generate
    :return: config with provided parameters
    """
    conf_path = os.path.join(os.path.dirname(__file__), 'neat-config')
    config = Config(DefaultGenome, DefaultReproduction, DefaultSpeciesSet, DefaultStagnation, conf_path)
    num_inputs = 12 + sum(instruments.values())
    config.set_num_inputs(num_inputs)

    return config


if __name__ == "__main__":
    main()
