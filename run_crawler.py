import logging
import subprocess


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    logging.info(proc_stdout)


subprocess_cmd('python manage.py startech_crawl')
subprocess_cmd('python manage.py ryans_crawl')
subprocess_cmd('python manage.py c_source_crawl')
subprocess_cmd('python manage.py ucc_crawl')
subprocess_cmd('python manage.py penguin_crawl')
subprocess_cmd('python manage.py pickaboo_crawl')
subprocess_cmd('python manage.py mke_crawl')
subprocess_cmd('python manage.py othoba_crawl')
subprocess_cmd('python manage.py rokomari_crawl')
subprocess_cmd('python manage.py hirakraja_crawl')
