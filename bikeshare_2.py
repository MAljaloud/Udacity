from itertools import combinations
from pickle import FALSE, TRUE
import time
from tkinter.messagebox import YES
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = [x.lower() for x in ['Chicago', 'New York', 'Washington']]
MONTHS = [x.lower() for x in ["January","February","March","April","May","June","July","August","September","October","November","December","All"]]
DAYS = [x.lower() for x in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","All"]]

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
    city = input('Please enter a city to analyze (Chicago, New York, Washington): ').lower().strip()
    if city not in CITIES:
         while city not in CITIES:
            print("Sorry, Invalid Input")
            city = input('Please enter a city to analyze (Chicago, New York, Washington): ').lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input('Please enter a month to analyze (eg March or All for all months): ').lower().strip()
    if month not in MONTHS:
         while month not in MONTHS:
           print("Sorry, Invalid Input")
           month = input('Please enter a month to analyze (eg March or All for all months): ').lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day to analyze (eg Sunday or type All to show all days): ').lower().strip()
    if day not in DAYS:
          while day not in DAYS:
           print("Sorry, Invalid Input")
           day = input('Please enter a day to analyze (eg Sunday or type All to show all days): ').lower().strip()

    print('-'*40)
    return city, month, day


def load_data(city, month, day, CITY_DATA):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    df[["Start Time", "End Time"]] = df[["Start Time", "End Time"]].apply(pd.to_datetime)
    if month != "all":
        df = df[df['Start Time'].dt.month_name().str.lower() == month]
    if day != "all":
        df = df[df["Start Time"].dt.day_name().str.lower() == day] 
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    months_count = df['Start Time'].groupby([df['Start Time'].dt.month_name()]).agg('count').sort_values(ascending=False)
    print("\nMonth/s and their count in descending order: \n" + months_count.to_string(index=FALSE,header=False))
          

    # display the most common day of week
    day_count = df['Start Time'].groupby([df['Start Time'].dt.day_name()]).agg('count').sort_values(ascending=False)
    print("\nDay\s and their count: \n" + day_count.to_string(index=FALSE,header=False))

    # display the most common start hour
    hours_count = df['Start Time'].groupby([df['Start Time'].dt.hour]).agg('count').sort_values(ascending=False)[:5]
    print("\nTop 5 Hours (24h format) and their count: \n" + hours_count.to_string(index=FALSE,header=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].groupby([df['Start Station']]).agg('count').sort_values(ascending=False)[:5]
    print("\nTop 5 Start stations and their count in descending order: \n" + start_station_count.to_string(index=FALSE,header=False))

    # display most commonly used end station
    end_station_count = df['End Station'].groupby([df['End Station']]).agg('count').sort_values(ascending=False)[:5]
    print("\nTop 5 End stations and their count in descending order: \n" + end_station_count.to_string(index=FALSE,header=False))

    # display most frequent combination of start station and end station trip
    start_end_station_count = df['End Station'].groupby([df['Start Station']+" / "+df['End Station']]).agg('count').sort_values(ascending=False)[:5]
    print("\nTop 5 Start-End stations combinations and their count in descending order: \n" + start_end_station_count.to_string(index=FALSE,header=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("\nThe total travel time: ")
    print(total_travel_time)
    # display mean travel time
    avgerage_travel_time = df["Trip Duration"].mean()
    print("\nThe average travel time: end")
    print(avgerage_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].groupby([df['User Type']]).agg('count').sort_values(ascending=False)[:5]
    print("\nUser types and their count: \n" + user_types_count.to_string(index=FALSE,header=False))

    if city == "washington":
        print("\nGender and year of birth is not applicable in case of washington")
    else:
         # Display counts of gender
         gender_count = df['User Type'].groupby([df['Gender']]).agg('count').sort_values(ascending=False)[:5]
         print("\nUser types and their count: \n" + gender_count.to_string(index=FALSE,header=False))
         # Display earliest, most recent, and most common year of birth
         earliest_birth_year=int(max(df["Birth Year"]))
         print("\nThe earliest birth year is ")
         print(earliest_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data."""

    user_choice = input("Would you like to see raw data? ").lower().strip()
    i=6
    j=1
    if user_choice == "yes":
        while user_choice == "yes" and i <= df["User Type"].count():
            print(df.iloc[j:i])
            i=i+5
            j=j+5
            user_choice = input("Would you like to see more raw data? ").lower().strip()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day, CITY_DATA)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
