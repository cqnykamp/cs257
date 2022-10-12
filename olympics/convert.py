'''
Written by Charles Nykamp 10/11/22

The source data can be found on Kaggle:
https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

def main():

    nocs = {}

    with open('kaggle_olympic_games/noc_regions.csv') as noc_regions_input_csv:
        reader = csv.reader(noc_regions_input_csv, delimiter=',', quotechar='"')
        heading_row = next(reader)

        for row in reader:
            abbreviation = row[0]
            full_name = row[1]
            nocs[abbreviation] = [len(nocs), abbreviation, full_name]

    
    athletes = {}
    events = {}
    olympic_games = {}


    with open('kaggle_olympic_games/athlete_events.csv') as athlete_event_input_csv:
        reader = csv.reader(athlete_event_input_csv, delimiter=',', quotechar='"')
        heading_row = next(reader)
        for row in reader:

            athlete_name = row[1]
            game_year = row[9]
            game_season = row[10]
            city = row[11]
            event_name = row[13]
            team_name = row[6]
            noc_abbreviation = row[7]

            # Some NOCs weren't included in noc_regions.csv, so we'll fill them in here
            if not noc_abbreviation in nocs:
                nocs[noc_abbreviation] = [len(nocs), noc_abbreviation, team_name]


            # === Athletes ===
            if athlete_name not in athletes:


                # Remove parts of the name that are wrapped in double quotes
                split_by_nickname = athlete_name.split('"')

                name_without_nickname = athlete_name
                if len(split_by_nickname) > 1:
                    name_without_nickname = split_by_nickname[0].strip(" ") + " " + split_by_nickname[-1].strip(" ")


                # Remove parts of the name that are inside parentheses
                name_without_parens = ""
                inside_paren = False
                for ch in name_without_nickname:
                    if ch == '(':
                        assert not inside_paren
                        inside_paren = True
                    elif ch == ')':
                        inside_paren = False

                    elif not inside_paren:
                        name_without_parens += ch


                # The first word is the given name, the rest is the surname
                words_in_name = name_without_parens.split(" ")
                athlete_first_name = words_in_name[0]
                athlete_last_name = " ".join(words_in_name[1:])

                athletes[athlete_name] = [len(athletes), athlete_first_name, athlete_last_name]


            # ==== Events table =====
            if not event_name in events:
                events[event_name] = [len(events), event_name]


            # ==== Olympic games table ====
            if not (game_year, game_season) in olympic_games:
                olympic_games[(game_year, game_season)] = [len(olympic_games), game_year, game_season, city]


    with open('athletes.csv', 'w') as athletes_output_file:
        writer = csv.writer(athletes_output_file)
        for athlete_data in athletes.values():
            writer.writerow(athlete_data)

    with open('events.csv', 'w') as events_output_file:
        writer = csv.writer(events_output_file)
        for event_data in events.values():
            writer.writerow(event_data)

    with open('nocs.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        for data in nocs.values():
            writer.writerow(data)

    with open('olympic_games.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        for data in olympic_games.values():
            writer.writerow(data)

    with open('game_event_athlete_results.csv', 'w') as output_file, \
        open('kaggle_olympic_games/athlete_events.csv') as athlete_event_input_csv:

        reader = csv.reader(athlete_event_input_csv, delimiter=',', quotechar='"')
        heading_row = next(reader)
        writer = csv.writer(output_file)

        for row in reader:
            athlete_id = athletes[row[1]][0]
            game_id = olympic_games[(row[9], row[10])][0]
            event_id = events[row[13]][0]
            noc_id = nocs[row[7]][0]

            medal = row[14]
            athlete_height = row[4]
            athlete_weight = row[5]

            writer.writerow([game_id, event_id, athlete_id, medal, noc_id, athlete_height, athlete_weight])


if __name__ == "__main__":
    main()

