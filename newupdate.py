import time
import pandas as pd
import numpy as np
import datetime as dt
import click

# This is change 1, a1
# This is change 1, a2. These changes will be the first commit.

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def choice(prompt, choices=('y', 'n')):
    """Returns a valid input from user."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'end':
            raise SystemExit
        if user_input in choices:
            return user_input
        if ',' in user_input:
            user_input = [i.strip().lower() for i in user_input.split(',')]
            if all([i in choices for i in user_input]):
                return user_input
        prompt = "Incorrect input, enter a valid option:\n>"


    return choice


def get_filters():
    """Ask user to specify city and filters, month and weekday.
    Returns:
        (str) city -name of the city to analyze
        (str) month -name of the month to filter
        (str) day -name of the day to filter
    """

    print("\n\nHere's some data, enjoy\n")

    print("Type end at any time if you would like to stop and end the program.\n")

    while True:
        city = choice("\nChoose a city; "
                      "New York City, Chicago or Washington? \n>", CITY_DATA.keys())
        month = choice("\nChoose a month from January to June or type 'all' for all months. \n>",
                       months + ('all',))
        day = choice("\nChoose a weekday or type 'all' for all days. \n>", weekdays + ('all',))

        # Confirm user input
        confirmation = choice("\nConfirm that you would like to apply "
                              "the following filters to the bikeshare data."
                              "\n\n City: {}\n Month: {}\n Weekday"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nTry again")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Load data for the specified filters of city, month and
       day whenever applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter
        (str) day - name of the day of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nLoading data.")
    start_time = time.time()

    # Filter the data according to the selected city filter
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # Reorganise DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Create columns to display stats
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter data according to month and weekday into two new DataFrames
    if month == 'all':
        pass
    elif isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if day == 'all':
        pass
    elif isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Display stats on the most frequent times of travel."""

    print('\nDisplaying stats on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # Display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The most common day of the week is: ' +
          str(most_common_day) + '.')

    # Display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: ", most_common_end_station)

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " - " + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print("Most frequent combination of start station and end station trip: ", most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("Counts of user types: \n", user_types_count)

    # Display counts of gender if available in the data
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print("Counts of gender: \n", gender_count)
    else:
        print("\nGender data not available.")

    # Display earliest, most recent, and most common year of birth if available in the data
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print("Earliest birth year: ", earliest_birth_year)

        most_recent_birth_year = int(df['Birth Year'].max())
        print("Most recent birth year: ", most_recent_birth_year)

        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("Most common birth year: ", most_common_birth_year)
    else:
        print("\nBirth year data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data if user enters 'yes', and continue with the program if user enters 'no'."""
    start_index = 0
    while True:
        display_data = input("Would you like to see the first 5 rows of data? Enter 'yes' or 'no': \n")
        if display_data.lower() != 'yes':
            break
        print(df.iloc[start_index:start_index+5])
        start_index += 5

        if input("Do you want to keep printing raw data?\n\n[y]Yes\n[n]No\n\n>").lower() == 'y':
            continue
        else:
            break
    return


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = choice("\nDo you want to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()