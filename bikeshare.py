import time
import pandas as pd
import numpy as np
import csv

month_dict = {0: 'all', 1:'January', 2: 'February', 3:'March', 4: 'April', 5:'May', 6: 'June' }
day_dict = {0:'all', 1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
city_data = { 'Chicago': 'chicago.csv',
              'New-York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

	# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('What city would you like to know about.\n VALID Citys are Chicago, New-York, Washington ')
    city = input().strip().title()
    while city != "Chicago" and city != "New-York" and city != "Washington":
        print("Please enter one of the VALID citys")
        city = input().strip().title()

	# get user input for month (all, january, february, ... , june)
    print("What month are you interested in ? VALID months: All, January, February, ... , June")
    month = input().strip().title()
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    
    while month not in months :
        print("Please enter a VALID month")
        month = input().strip().title()

	# get user input for day of week (all, monday, tuesday, ... sunday)
    print("What day of the week are you interested in ? VALID day: All, Monday, Tuesday, ... Sunday")
    day = input().strip().title()
    days = ['All', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    while day not in days:
        print("Please enter a VALID day")
        day = input().strip().title()
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city_data[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.dayofweek

    df['hour'] = df['Start Time'].dt.hour

    df['station_comb'] = 'From '+ df['Start Station'] + ' to ' + df['End Station']

    df['duration'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])      
  
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day = days.index(day) + 1 
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].value_counts().index[0]
    print('\nThe most common rental month is: ' + month_dict[most_month])

    # display the most common day of week
    most_day = df['day_of_week'].value_counts().index[0]
    print('\nThe most common rental day of week is: ' + day_dict[most_day])

    # display the most common start hour
    most_hour = df['hour'].value_counts().index[0]
    print('\nThe most common start hour is: ' + str(most_hour))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_startSt = df['Start Station'].value_counts().index[0]
    print('\nThe most commonly used start station is: ' + most_startSt)    

    # display most commonly used end station
    most_endSt = df['End Station'].value_counts().index[0]
    print('\nThe most commonly used end station is: ' + most_endSt) 

    # display most frequent combination of start station and end station trip
    most_combSt = df['station_comb'].value_counts().index[0]
    print('\nThe most frequent combination of start station and end station trip is: ' + most_combSt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['duration'].sum()
    print('\nThe total travel time is: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['duration'].mean()
    print('\nThe avarafe travel time is: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The count of user types is: ' + str(user_type))

    # Display counts of gender
    try:        
        gender = df['Gender'].value_counts()
        print('The count of genders is: ' + str(gender))
    except KeyError:
        print('For Washington there is no information about gender.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_byear = int(df['Birth Year'].min())
        print('\nThe oldest customer is from: ' + str(earliest_byear))
        recent_byear = int(df['Birth Year'].max())
        print('\nThe youngest customer is from: ' + str(recent_byear))    
        common_byear = int(df['Birth Year'].value_counts().index[0])
        print('\nThe most common year of birth is: ' + str(common_byear))
    except KeyError:
        print('For Washington there is no information about birth year.')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()    
        df = load_data(city, month, day)
        while df.empty == True:
            print('\nThere is no data for your selection, please select something else')            
            city, month, day = get_filters()
            df = load_data(city, month, day)            
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes = Y or no = N (or anything else) .\n')
        if restart != 'Y' and restart != 'y':
            break

if __name__ == "__main__":
	main()
