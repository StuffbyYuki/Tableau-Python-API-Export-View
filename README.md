# Tableau Python API

This is a python script based off of an example in [Tableau Server Client (Python)](https://github.com/tableau/server-client-python)

The script in the link above is not working as is (as of 11/13/2020), so this script is to help export csv/png/pdf of a view in your Tableau server.

## Prerequisites

You need to have installed Python 3.5 or later.

You also need to install tableau server client python package.

To install the package, type the following:

```
pip install tableauserverclient
```
or
```
pip install -r requirements.txt
```

## Installing

When you run the script, you can use the command like the following:


```
python export_view.py -s SITENAME -u USERNAME -p PASSWORD -v YOURVIEWNAME --csv -f YOURFILENAME.csv
```

And you can also add other arguments as neccesary. Look into the code for details.

One thing to note is that you cannot export a csv and a png/pdf or vice verse in one run.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

