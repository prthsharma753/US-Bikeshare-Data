import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while(city.lower() not in ['chicago', 'new york', 'washington']):
        city = input('Enter the city you wish to explore the data of: ')

    # get user input for month (all, january, february, ... , june)
    month = ''
    while(month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']):
        month = input('\nWhich month\'s data?[All, January, February, March, April, May, June]: ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while(day.lower() not in ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        day = input('\nWhich day\'s data?[All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]: ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['Start Time'].dt.month.mode())
    common_month = months[index - 1]
    print('The most common month is {}.'.format(common_month))

    # display the most common day of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    common_day = df['Start Time'].dt.weekday_name.mode().to_string(index=False)

    print('The most common day is {}.'.format(common_day))

    # display the most common start hour
    most_pop_hour = int(df['Start Time'].dt.hour.mode())
    if most_pop_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_pop_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_pop_hour
    elif 13 <= most_pop_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_pop_hour - 12
    print('The most popular hour of day for start time is {}{}.'.format(pop_hour_readable, am_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode().to_string(index = False)

    print('The most popular start station is {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode().to_string(index = False)

    print('The most popular end station is {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    try:
        trp_lst = []
        for i, j in zip(df['Start Station'], df['End Station']):
            trp_lst.append(i+j)
        print("\n\nMost Popular Trip is {}".format(mode(trp_lst)))
    except Exception:
        print("No most popular Trip")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_convert(seconds):
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)

    hours = seconds // 3600
    seconds = seconds % 3600

    minutes = seconds // 60
    seconds = seconds % 60
    return ([days, hours, minutes, seconds])

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    total_time = time_convert(seconds)
    print("\nTotal duration of trip: {} days {} hours {} minutes {} seconds".format(total_time[0],
    total_time[1], total_time[2], total_time[3]))

    # display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    mean = time_convert(seconds)
    print("\nAverage travel time: {} days {} hours {} minutes {} seconds".format(mean[0],
    mean[1], mean[2], mean[3]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].unique()
    user_types_count = df['User Type'].value_counts()
    print('\nThere are {} {} and {} {}.'.format(user_types_count[0], user_types[0], user_types_count[1],
    user_types[1]))

    # Display counts of gender
    try:
        gender_types = df['Gender'].unique()
        gender_types_count = df['Gender'].value_counts()
        print('\nThere are {} {} and {} {}.'.format(gender_types_count[0], gender_types[0], gender_types_count[1],
        gender_types[1]))
    except Exception:
        print('\nInformation regarding gender of users is not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        mode = int(df['Birth Year'].mode())
        print('The oldest users are born in {}.\nThe youngest users are born in {}.'
              '\nThe most popular birth year is {}.'.format(oldest, youngest, mode))
    except Exception:
        print('\nInformation regarding birth year of users is not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    start = 0
    end = 5
    check = True
    while check:
        display = input("\nWould you like to view individual trip data? Enter 'yes' or 'no'.")
        if (display.lower() == 'yes' or 'no'):
            break
        else:
            print('Invalid Input')
    if display.lower() == 'yes':
        print(df[df.columns].iloc[start:end])
        more = ''
        while more != 'no':
            check_more = True
            while check_more:
                more = input("\nDo you wanna see few more? Enter 'yes' or 'no'.")
                if (more.lower() == 'yes' or 'no'):
                    break
                else:
                    print('Invalid Input')
            if more.lower() == 'yes':
                start += 5
                end += 5
                print(df[df.columns].iloc[start:end])
            elif more.lower() == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
