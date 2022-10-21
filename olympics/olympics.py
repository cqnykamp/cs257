'''
A CLI program that display Olympics-related data from a database
Written by Charles Nykamp for Software Design class at Carleton College, October 2022
'''

import config
import psycopg2
import sys


# Uses psycopg2 to connect to a database
def get_connection():
    try:
        return psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


# Returns all the athletes from a NOC
def get_athletes_from_noc(noc_name):

    athletes = []

    query = '''
        SELECT athletes.given_name, athletes.surname
        FROM athletes
        INNER JOIN game_event_athlete_results
        ON game_event_athlete_results.athlete_id = athletes.id
        INNER JOIN nocs
        ON game_event_athlete_results.noc_id = nocs.id
        AND nocs.name ILIKE CONCAT('%%', %s, '%%')
    '''

    try:
        # Get database connection and run query
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (noc_name,))

        # Iterate over the query results to produce the list of athlete names.
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            athletes.append((given_name, surname))

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes


# Returns a list of NOCs, in decreasing order of gold medals earned
def get_nocs_ranked_by_gold():
    nocs = []

    query ='''
        SELECT nocs.name, COUNT(game_event_athlete_results.medal)
        FROM nocs
        LEFT JOIN game_event_athlete_results
        ON game_event_athlete_results.noc_id = nocs.id
        AND game_event_athlete_results.medal = 'Gold'
        LEFT JOIN athletes
        ON athletes.id = game_event_athlete_results.athlete_id
        GROUP BY nocs.name
        ORDER BY COUNT(game_event_athlete_results.medal) DESC;
    '''

    try:

        # Get database connection and run query
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        # Add each row into the returned list
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            nocs.append((given_name, surname))

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return nocs


# Returns a list of athletes who have participated in a specified event.
# The parameter 'event_name' doesn't have to be the whole name of the event, it can be a substring.
# This function will include all events who match the substring
# The parameter 'athlete_limit' puts a cap on how many total athletes can be returned
def get_athletes_in_event(event_name, athlete_limit):
    assert isinstance(athlete_limit, int)

    athletes = []

    query ='''
        SELECT athletes.given_name, athletes.surname, events.name, COUNT(athletes.id)
        FROM athletes
        INNER JOIN game_event_athlete_results
        ON athletes.id = game_event_athlete_results.athlete_id
        INNER JOIN events
        ON events.name ILIKE CONCAT('%%', %s, '%%')
        AND game_event_athlete_results.event_id = events.id
        GROUP BY athletes.given_name, athletes.surname, events.name
        ORDER BY COUNT(athletes.id) DESC
        LIMIT %s;
    '''

    try:

        # Get database connection and run query
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (event_name, athlete_limit))


        # Add each row to the athletes list
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            event = row[2]            
            num_times_participated = row[3]

            new_data = (num_times_participated, given_name, surname, event)
            athletes.append(new_data)

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes
    

# The main function of this CLI
# Assumes that args are the relevant arguments from the perspective of the CLI
def run(args):

    if '--help' in sys.argv or '-h' in sys.argv:
        # Display the usage statement
        with open('./usage.txt') as usage_statement:
            print(usage_statement.read())
        return

    if len(args) < 1:
        print('No command specified.')
        print('See --help for usage info.')
        return


    if args[0] == 'athletes-from':
        
        # Find NOC name from argument
        if len(args) < 2:
            print('The "athletes-from" command requires one argument: the name of a national olympic committee.')
            print('See --help for usage info.')
            return
        noc_name = " ".join(args[1:])

        # Query the database and display the results
        athletes = get_athletes_from_noc(noc_name)
        for athlete in athletes:
            print(f'{athlete[0]} {athlete[1]}' )



    elif args[0] == 'noc_rank':
        
        # Query the database and display the results
        nocs_ranked = get_nocs_ranked_by_gold()
        for (noc_name, golds) in nocs_ranked:
            print(f'{noc_name}, {golds}')
    

    elif args[0] == 'athletes-in':

        if len(args) < 2:
            print('The "athletes-in" command requires one argument: the name of a Olympics event')
            print('See --help for usage info.')
            return

        # Set the limit, using the argument if given
        limit = 25
        has_specified_limit = False
        if len(args) > 2 and (args[2] == '--limit' or args[2] == '-l'):
            has_specified_limit = True

            try:
                limit = int(args[3])
                if limit <= 0:
                    print(f'{args[2]} must have a positive integer value.')
                    print('See --help for usage info.')
                    return

            except:
                print(f'{args[2]} must have a positive integer value.')
                print('See --help for usage info.')
                return


        # Compose the event name, making sure not to include --limit 
        # if it exists
        if has_specified_limit:
            event_name = " ".join(args[1 : -2])
        else:
            event_name = " ".join(args[1:])
        

        # Query the database and display the results
        athletes = get_athletes_in_event(event_name, limit)
        for athlete in athletes:
            print(f'{athlete[0]} {athlete[1]} {athlete[2]} ({athlete[3]})')

        if len(athletes) == 0:
            print(f'There are no events whose name contains "{event_name}".')



    else:
        print(f'No command "{args[0]}". ')
        print('See --help for usage info.')





if __name__ == "__main__":
    run(sys.argv[1:])

