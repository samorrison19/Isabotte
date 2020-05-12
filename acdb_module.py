# Interface with anch.db - currently bug and fish table
# Ideas for future:
# ~ Create tags to identify butterflies/beetles etc with names that don't
#   include their type?
# ~ Method to recombine bugs with two month blocks? <- Wonder wtf that means
import sqlite3
import calendar as cal


conn = sqlite3.connect('acnh.db')
c = conn.cursor()


# OUTPUT METHODS
def display_bugs(buglist):
    # Quick and dirty print all
    columns = ('id', 'name', 'location', 'price', 'start month', 'end month',
               'start hour', 'end hour')
    for item in columns:
        print(str(item)[:12].center(15), end='')
    print()
    for bug in buglist:
        for item in bug:
            print(str(item)[:12].center(15), end='')
        print()


# def bugs_to_comment(buglist):
#     columns = ('id', 'name', 'location', 'price', 'start month', 'end month',
#                'start hour', 'end hour')
#     comment = ('')
#     for item in columns:
#         comment = comment + str(item)[:12].center(15)
#     comment = comment + '\n'
#     for bug in buglist:
#         for item in bug:
#             comment = comment + str(item)[:12].center(15)
#         comment = comment + '\n'
#     return comment

# def short_comment(buglist):
#     # Displays only bugs, price, time, location
#     comment = ''
#     for bug in buglist:
#         if bug[6] == 0:
#             hours = '-- All day --'
#         else:
#             if bug[6] > 12:
#                 beg_hr = f'{str(bug[6]-12)} PM'
#             else:
#                 beg_hr = f'{str(bug[6])} AM'
#             if bug[7] > 12:
#                 end_hr = f'{str(bug[7]-12)} PM'
#             else:
#                 end_hr = f'{str(bug[7])} AM'
#             hours = f'{beg_hr} to {end_hr}'
#         comment = f'{comment}\n{bug[1].rjust(26)}|{str(bug[3]).center(5)}'\
#                   f'|{hours.center(14)}|{bug[2][:24].ljust(24)}'
#     return comment


def mobile_comment_bug(buglist):
    # Prints bug list to be formatted for 38 char wide mobile viewing
    # just name, price, time, location
    comment = ''
    for bug in buglist:
        if bug[6] == 0:
            hours = '-All day-'
        else:
            if bug[6] > 12:
                beg_hr = f'{str(bug[6]-12)}pm'
            else:
                beg_hr = f'{str(bug[6])}am'
            if bug[7] > 12:
                end_hr = f'{str(bug[7]-12)}pm'
            else:
                end_hr = f'{str(bug[7])}am'
            hours = f'{beg_hr} - {end_hr}'
        price = str(bug[3]) + ' bells'
        comment = f'{comment}\n\n{bug[1].rjust(26)}|{price.ljust(11)}'\
                  f'\n{bug[2][:24].rjust(26)}|{hours.ljust(11)}'
    return comment


def long_mobile_comment_bug(buglist):
    # Prints bug list to be formatted for 38 char wide mobile viewing
    # Name, Price, Month, Time, Location
    comment = ''
    for bug in buglist:
        # assign hour appropriately
        if bug[6] == 0:
            hours = '-All day-'
        else:
            if bug[6] > 12:
                beg_hr = f'{str(bug[6]-12)}pm'
            else:
                beg_hr = f'{str(bug[6])}am'
            if bug[7] > 12:
                end_hr = f'{str(bug[7]-12)}pm'
            else:
                end_hr = f'{str(bug[7])}am'
            hours = f'{beg_hr} - {end_hr}'
        # month string
        if bug[4] == 1 and bug[5] == 12:
            months = '-All Year-'
        else:
            months = f'{cal.month_abbr[bug[4]]} to {cal.month_abbr[bug[5]]}'

        # price string
        price = str(bug[3]) + ' bells'
        # price + mo + hours
        middle = f'{price} | {months} | {hours}'

        # assemble
        comment = f'{comment}\n\n|{bug[1].center(38)}|'\
                  f'\n|{middle.center(38)}|'\
                  f'\n|{bug[2][:34].center(38)}|'
    return comment


def mobile_comment_fish(fishlist):
    comment = ''
    for fish in fishlist:
        # Make hour into string
        if int(fish[7]) == 0:
            hours = '24hr'
        else:
            if int(fish[7]) > 12:
                beg_hr = f'{str(fish[7]-12)}p'
            else:
                beg_hr = f'{str(fish[7])}a'
            if fish[8] > 12:
                end_hr = f'{str(fish[8]-12)}p'
            else:
                end_hr = f'{str(fish[8])}a'
            hours = f'{beg_hr}-{end_hr}'
        # Make month into string

        # Make price into string
        price = str(fish[4]) + 'b'

        # Assemble into rows
        top = f'{fish[1][:18]}|{price.ljust(6)}'
        middle = f'{fish[2][:5]}|{fish[3][:8]}|{hours.ljust(6)}'

        comment = f'{comment}\n{top.rjust(25)}\n'\
                  f'{middle.rjust(25)}\n'
    return comment


def long_mobile_comment_fish(fishlist):
    comment = ''
    for fish in fishlist:
        # Make hour into string
        if int(fish[7]) == 0:
            hours = '-All day-'
        else:
            if int(fish[7]) > 12:
                beg_hr = f'{str(fish[7]-12)}pm'
            else:
                beg_hr = f'{str(fish[7])}am'
            if fish[8] > 12:
                end_hr = f'{str(fish[8]-12)}pm'
            else:
                end_hr = f'{str(fish[8])}am'
            hours = f'{beg_hr} - {end_hr}'
        # Make month into string
        if fish[5] == 1 and fish[6] == 12:
            months = '-All Year-'
        else:
            months = f'{cal.month_abbr[fish[5]]} to {cal.month_abbr[fish[6]]}'
        # Make price into string
        price = str(fish[4]) + 'b'

        # Assemble into rows
        top = f'{fish[1]} || {price}'
        middle = f'{fish[2]} || {fish[3]}'
        bottom = f'{months} || {hours}'

        comment = f'{comment}\n|{top.center(30)}|\n'\
                  f'|{middle.center(30)}|\n'\
                  f'|{bottom.center(30)}|\n'
    return comment


# HELPER METHOD
def id_to_string(idlist):
    # Turn a list of ID tuples into a string in format '(1,2,3)' that
    # is SQL-query-ready
    string = ','.join(map(str, idlist))
    string = '({})'.format(string.replace('(', '').replace(',)', ''))
    return string


def get_with_ids(table, idstring):
    # Return all items in given table with id in idstring
    # idstring will have to be sent to id_to_string() first - can't be list
    c.execute("""SELECT * FROM {}
                WHERE id IN {}""".format(table, idstring))
    return c.fetchall()


# GENERIC GETS
def get_all(table, sortby='price', order='DESC'):
    # Return all in given table - default sort by price descending
    # sort can be name of any column, order can be 'DESC' or 'ASC'
    c.execute("SELECT * FROM {} ORDER BY {} {};".format(table, sortby, order))
    return c.fetchall()


def get_month_ids(table, month, string=True):
    # Given a table (STRING), month int, return a string of all ids of items
    # available in that month.
    # This string can be passed into SQL queries to sort results.
    # set string=False to get a list of tuples of ids instead

    # Get beginning to December if month wraps
    c.execute("""SELECT id FROM {}
                WHERE month_beg > month_end
                AND {} BETWEEN month_beg AND 12;
                """.format(table, month))
    ids = c.fetchall()

    # Get January to end if month wraps
    c.execute("""SELECT id FROM {}
                WHERE month_beg > month_end
                AND {} BETWEEN 0 AND month_end;
                """.format(table, month))
    ids = ids + c.fetchall()

    # Get beg to end if no month wrapping
    c.execute("""SELECT id FROM {}
                WHERE month_beg < month_end
                AND {} BETWEEN month_beg AND month_end;
                """.format(table, month))
    ids = ids + c.fetchall()

    # Get current month (Salmon/King Salmon special case)
    c.execute("""SELECT id FROM {}
                WHERE month_beg == {}
                OR month_end == {};
                """.format(table, month, month))
    ids = ids + c.fetchall()
    if string:
        return id_to_string(ids)
    else:
        return ids


def get_hour_ids(table, month, hour):
    # Given a table (STRING) month int and hour int,
    # return a string of all ids of items
    # available in that month and hour.
    # This string can be passed into SQL queries to sort results.
    month_ids = get_month_ids(table, month)
    c.execute("""SELECT id FROM {}
                WHERE id IN {}
                AND hr_beg > hr_end
                AND {} BETWEEN hr_beg AND 24;
                """.format(table, month_ids, hour))
    ids = c.fetchall()

    c.execute("""SELECT id FROM {}
                WHERE id IN {}
                AND hr_beg > hr_end
                AND {} BETWEEN 0 AND hr_end;
                """.format(table, month_ids, hour))
    ids = ids + c.fetchall()

    c.execute("""SELECT id FROM {}
                WHERE id IN {}
                AND hr_beg < hr_end
                AND {} BETWEEN hr_beg AND hr_end;
                """.format(table, month_ids, hour))
    ids = ids + c.fetchall()

    return id_to_string(ids)


def get_in_month(table, month, sortby='price', order='DESC'):
    # Return a list of tuples of all items in a given table and month (int)
    # sorted by column passed in. Order can be 'ASC' or 'DESC'
    id_string = get_month_ids(table, month)
    c.execute("""SELECT * FROM {}
                WHERE id IN {}
                ORDER BY {} {};
                """.format(table, id_string, sortby, order))
    return c.fetchall()


def get_in_hour(table, month, hour, sortby='price', order='DESC'):
    # Return a list of tuples of all items in a given table, month int, 
    # and hour int, sorted by column passed in - default is by price descending.
    # Order can be 'ASC' or 'DESC'
    id_string = get_hour_ids(table, month, hour)
    c.execute("""SELECT * FROM {}
                 WHERE id IN {}
                 ORDER BY {} {};
                 """.format(table, id_string, sortby, order))
    return c.fetchall()


def get_with_precise_name(table, name, sortby='price', order='DESC'):
    # Return all items with name exactly matching name given in given table.
    camel_name = name.title()
    c.execute("""SELECT * FROM {}
                WHERE name = '{}'
                ORDER BY {} {};""".format(table, camel_name, sortby, order))
    return c.fetchall()


def get_with_name(table, name, sortby='price', order='DESC'):
    # Return all items with a given string in the name in given table,
    # i.e. "butter" selects all bugs with "butterfly" in their name
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    c.execute("""SELECT * FROM {}
                WHERE name LIKE '%{}%'
                ORDER BY {} {};""".format(table, name, sortby, order))
    return c.fetchall()


def get_at_location(table, location, sortby='price', order='DESC'):
    # Return all items at given location in given table,
    # looks for string in location column,
    # i.e. "sea" also selects "sea (rainy days)"
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    c.execute("""SELECT * FROM {}
                WHERE location LIKE '%{}%'
                ORDER BY {} {};""".format(table, location, sortby, order))
    return c.fetchall()


def get_last_chance(table, month, sortby='price', order='DESC'):
    if month==12:
        nextmonth = 1
    else:
        nextmonth = month+1
    current = get_month_ids(table, month, string=False)
    next = get_month_ids(table, nextmonth, string=False)
    # return list(set(current) - (set(next)))
    pass
# *** NOT FINISHED ***


# BUG METHODS

def bugs_in_month(month, sortby='price', order='DESC'):
    # Return a list of tuples of all bugs in a given month int sorted by column
    # passed in - default is by price descending. Order can be 'ASC' or 'DESC'
    return get_in_month('bugs', month, sortby, order)


def bug_hour_ids(month, hour):
    # Given a month int and hour int, return a string of all ids of bugs
    # available in that month and hour.
    # This string can be passed into SQL queries to sort results.
    return id_to_string(get_hour_ids('bugs', month, hour))


def bugs_in_hour(month, hour, sortby='price', order='DESC'):
    # Return a list of tuples of all bugs in a given month int and hour int
    # sorted by column passed in - default is by price descending.
    # Order can be 'ASC' or 'DESC'
    return get_in_hour('bugs', month, hour, sortby, order)


def all_bugs(sortby='price', order='DESC'):
    # Return all bugs - default sort by price descending
    # sort can be name of any column, order can be 'DESC' or 'ASC'
    c.execute("SELECT * FROM bugs ORDER BY {} {};".format(sortby, order))
    return c.fetchall()


def bugs_at_location(location, sortby='price', order='DESC'):
    # Return all bugs at given location, looks for string in location column,
    # i.e. "flying" also selects "Flying by purple flowers"
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    return get_at_location('bugs', location, sortby, order)


def bug_with_precise_name(name, sortby='price', order='DESC'):
    # Return all bugs with name exactly matching name given.
    return get_with_precise_name('bugs', name, sortby, order)


def bugs_with_name(name, sortby='price', order='DESC'):
    # Return all bugs with a given string in the name,
    # i.e. "butter" selects all bugs with "butterfly" in their name
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    return get_with_name('bugs', name, sortby, order)


# FISH METHODS
def all_fish(sortby='price', order='DESC'):
    # Return all fish - default sort by price descending
    # sort can be name of any column, order can be 'DESC' or 'ASC'
    c.execute("SELECT * FROM fish ORDER BY {} {};".format(sortby, order))
    return c.fetchall()


def fish_in_month(month, sortby='price', order='DESC'):
    # Return a list of tuples of all fish in a given month int sorted by column
    # passed in - default is by price descending. Order can be 'ASC' or 'DESC'
    return get_in_month('fish', month, sortby, order)


def fish_in_hour(month, hour, sortby='price', order='DESC'):
    # Return a list of tuples of all fish in a given month int and hour int
    # sorted by column passed in - default is by price descending.
    # Order can be 'ASC' or 'DESC'
    return get_in_hour('fish', month, hour, sortby, order)


def fish_at_location(location, sortby='price', order='DESC'):
    # Return all fish at given location, looks for string in location column,
    # i.e. "sea" also selects "sea (rainy days)"
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    return get_at_location('fish', location, sortby, order)


def fish_with_precise_name(name, sortby='price', order='DESC'):
    # Return all fish with name exactly matching name given.
    return get_with_precise_name('fish', name, sortby, order)


def fish_with_name(name, sortby='price', order='DESC'):
    # Return all fish with a given string in the name,
    # i.e. "butter" selects all bugs with "butterfly" in their name
    # default sort by price descending
    # Sort can be name of any column, order can be 'DESC' or 'ASC'
    return get_with_name('fish', name, sortby, order)


if __name__ == '__main__':
    # def bugs_last_chance(month):
    #     this_month = bug_month_ids(month)
    #     if month != 12:
    #         next_month = bug_month_ids(month+1)
    #     else:
    #         next_month = bug_month_ids(1)
    #     pass

    # c.execute("""SELECT * FROM bugs""")
    # firefly = c.fetchall()
    # for bug in firefly:
    #     print(bug)

    # butt = bugs_with_name('beetle')
    # for bugs in butt:
    #     print(bugs)
    
    # display_bugs(bugs_in_hour(4, 20))
    pass
