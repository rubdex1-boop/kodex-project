import threading
import main
import news


def run_main():
    main.run()


def run_news():
    news.run()


if __name__ == "__main__":
    t1 = threading.Thread(target=run_main)
    t2 = threading.Thread(target=run_news)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
