import logging


def setup_logs(name='local'):

    if hasattr(setup_logs, "_setup"):
        return True

    setattr(setup_logs, "_setup", True)

    logging.root.setLevel(logging.INFO)

    logging.basicConfig(
        format=f'[{name}] %(asctime)s - %(message)s: ',
        level=logging.INFO
    )

