
import csv

def main():
    
    athletes = {}
    athlete_index = 0
    # count_commas = 0

    events = {}
    event_index = 0

    nocs = {}
    noc_index = 0

    olympic_games = {}
    olympic_game_index = 0

    with open('kaggle_olympic_games/athlete_events.csv') as athlete_event_input_csv:
        reader = csv.reader(athlete_event_input_csv, delimiter=',', quotechar='"')
        heading_row = next(reader)
        for row in reader:

            athlete_name = row[1]
            year = row[]

            if athlete_name not in athletes:

                split_by_nickname = athlete_name.split('"')
                # print(split_by_nickname)
                # assert len(split_by_nickname) <= 3

                relevant_name = athlete_name
                if len(split_by_nickname) > 1:
                    relevant_name = split_by_nickname[0].strip(" ") + " " + split_by_nickname[-1].strip(" ")

                # print(relevant_name)

                name_without_parens = ""
                inside_paren = False
                # print(relevant_name)
                for ch in relevant_name:
                    if ch == '(':
                        assert not inside_paren
                        inside_paren = True
                    elif ch == ')':
                        inside_paren = False

                    elif not inside_paren:
                        name_without_parens += ch

                # if ',' in name_without_parens:
                #     count_commas += 1


                words_in_name = name_without_parens.split(" ")
                relevant_words = []

                athlete_first_name = words_in_name[0]
                athlete_last_name = " ".join(words_in_name[1:])

                athletes[athlete_name] = [athlete_index, athlete_first_name, athlete_last_name]
                athlete_index += 1

            
            # ==== Game participation ====
            if not (athlete_name, ) in game_participation:


            # ==== Events table =====
            event_name = row[13]

            if not event_name in events:
                events[event_name] = [event_index, event_name]
                event_index += 1


            # ==== NOCs table ====
            noc_name = row[7]

            if not noc_name in nocs:
                nocs[noc_name] = [noc_index, noc_name]
                noc_index += 1


            # ==== Olympic games table ====
            game_year = row[9]
            game_season = row[10]
            city = row[11]

            if not (game_year, game_season) in olympic_games:
                olympic_games[(game_year, game_season)] = [olympic_game_index, game_year, game_season, city]
                olympic_game_index += 1
        
    
    # print(f"commas found: {count_commas}")

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

            medal = row[14]
            athlete_height = row[4]
            athlete_weight = row[5]

            writer.writerow([game_id, event_id, athlete_id, medal, athlete_height, athlete_weight])


        # for data in olympic_games.values():
        #     writer.writerow(data)


if __name__ == "__main__":
    main()

