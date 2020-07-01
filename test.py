def main():
    import sys
    max_lines = int(sys.argv[1])

    lines = []

    wordlist_fn = '/usr/share/dict/words'
    import subprocess
    proc = subprocess.Popen(['cat', wordlist_fn], stdout=subprocess.PIPE)
    for index, line in enumerate(proc.stdout):
        lines.append(line.decode('utf-8').rstrip())
        if index == max_lines:
            break
    proc.kill()

    from Matchmaker import Matchmaker
    from stringdist import levenshtein

    matchmaker = Matchmaker(
        lines[:max_lines // 2],
        lines[max_lines // 2:],
        levenshtein
    )
    matchmaker.marry()


if __name__ == '__main__':
    for _ in range(50):
        main()
