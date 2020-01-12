# Lottery Checker

If you love to play polish lottery (LOTTO) and you always choose same numbers, feel free to use this program.
No more tedious comparison of your lottery coupon numbers with lottery numbers drawn!

## Getting Started

* Download repo
* Create database for lottery numbers (/docs/db_model should help with that :) )
* Run main.py.
* Click the "Add new numbers" button, add your favourite lucky numbers that you always choose in the lottery and close the app.
* Done!

Each time you open LotteryChecker, it will scrap lotto data from https://www.lotto.pl/, compare it with your numbers in the database and let you know if you won.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Themes for tkinter
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI 
* [ttkthemes](https://pypi.org/project/ttkthemes/) - Themes for tkinter
* [sqlite3](https://www.sqlite.org/index.html) - Database library


## Authors
* [Mrooie](https://github.com/Mrooie)
*Standalone app creation in progress*

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details
