####
# This script demonstrates how to use the Tableau Server Client
# 
# This script is based off of https://github.com/tableau/server-client-python/blob/master/samples/export.py
#
# For more information about tableau api, please refer to https://tableau.github.io/server-client-python/docs/
# 
# To run the script, you must have installed Python 3.5 or later.
# 
# Use the command like the following:
# 
# python export_view.py -s SITENAME -u USERNAME -p PASSWORD -v YOURVIEWNAME --csv -f YOURFILENAME.csv
####

import argparse
import getpass
import logging
import tableauserverclient as TSC

def get_args():
    """Parsing arguments given by the user"""
    parser = argparse.ArgumentParser(description='Download image of a specified view.')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--site-id', '-si', required=False, help='content url for site the view is on')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('-p', default=None)
    parser.add_argument('--view-name', '-v', required=True, help='name of view to download an image of')
    parser.add_argument('--logging-level', '-l', required=False, choices=['debug', 'info', 'error'], default='error', help='desired logging level (set to error by default)')
    parser.add_argument('--filter', '-vf', required=False, metavar='COLUMN:VALUE', help='View filter to apply to the view')
    parser.add_argument('--file', '-f', required=False, help='filename to store the exported data')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pdf', dest='type', action='store_const', const=('populate_pdf', 'PDFRequestOptions', 'pdf', 'pdf'))
    group.add_argument('--png', dest='type', action='store_const', const=('populate_image', 'ImageRequestOptions', 'image', 'png'))
    group.add_argument('--csv', dest='type', action='store_const', const=('populate_csv', 'CSVRequestOptions', 'csv', 'csv'))

    args = parser.parse_args()

    return args

def main():
    # Get parsed arguments
    args = get_args()

    # Prompt the user to enter the password
    if args.p is None:
        password = getpass.getpass("Password: ")
    else:
        password = args.p

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # Step 1: Sign in to server.
    site_id = args.site_id
    if not site_id:
        site_id = ""
    tableau_auth = TSC.TableauAuth(args.username, password, site_id=site_id)
    server = TSC.Server(args.server)

    # The new endpoint was introduced in Version 2.5
    server.version = "2.8"  # at least 2.5 for exporting a view image, 2.8 for exporting csv file

    with server.auth.sign_in(tableau_auth):
        # Step 2: Query for the view that we want an image/csv of
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                         TSC.RequestOptions.Operator.Equals, args.view_name))
        all_views, pagination_item = server.views.get(req_option)
        if not all_views:
            raise LookupError("View with the specified name was not found.")
        view_item = all_views[0]

        (populate_func_name, option_factory_name, member_name, extension) = args.type
        populate = getattr(server.views, populate_func_name)
        option_factory = getattr(TSC, option_factory_name)

        if args.filter:
            options = option_factory().vf(*args.filter.split(':'))
        else:
            options = None
        if args.file:
            filename = args.file
        else:
            filename = 'out.{}'.format(extension)        

        populate(view_item, options)

        # Step 3: Export the file to the specified path/filename
        with open(filename, 'wb') as f:
            if member_name == 'csv':
                f.writelines(getattr(view_item, member_name))
            else:
                f.write(getattr(view_item, member_name))

if __name__ == '__main__':
    main()
