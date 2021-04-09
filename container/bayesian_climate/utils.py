import logging
import time

def toc(tic):
	toc = time.time()

	time_diff = toc - tic

	logging.info(f"Time passed is {time_diff} seconds.")
