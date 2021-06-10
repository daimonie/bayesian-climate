import logging
import matplotlib.pyplot as plt
import sys

def setup_log(name='local'):

    if hasattr(setup_log, "_setup"):
        return True

    setattr(setup_log, "_setup", True)

    logging.root.setLevel(logging.INFO)

    logging.basicConfig(
        format=f'[{name}] %(asctime)s - %(message)s',
        level=logging.INFO
    )


def savefig(filename):
	plt.savefig(filename)
	logging.info(f"Saved figure to {filename}.")


def startfig():
	plt.figure(figsize=(50,8))
	logging.info("Starting figure, high res/pixels")

def stop():
	logging.critical("Execution cancelled")
	sys.exit(0)