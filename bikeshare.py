import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june'] 

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
            # get user input, clean and validate
            city = input("Enter the city name Chicago, New York City or Washington\n").lower().strip()
            if city in CITY_DATA.keys():
                break
            else:
                print("City not found")               


    while True:
            # get user input, clean and validate
            month = input("Enter the month you want to investigate or all\n").lower().strip()
            if (month in MONTHS) or (month == "all"):
                break
            else:
                print("Invalid selection")   
   

    while True:
            # get user input, clean and validate
            day = input("Enter the day of the week you want to investigate or all\n").lower().strip()
            if (day in DAYS) or (day == "all"):
                break
            else:
                print("Invalid selection") 

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
    # load file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # use to_datetime to convert start time column
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # use start time column to parse month, day of week and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel    
    Args:
        (df) df - Pandas DataFrame containing city data filtered by month and day
    """  

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print("The most frequent month is :", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print("The most frequent day of week is :", common_day)

    # display the most common start hour
    common_start = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", common_start)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (df) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most frequently used start station :", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print("The most frequently used end station :", common_end_station)

    # display most frequent combination of start station and end station trip
    common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    
    print("The most frequently used start station and end station : {}, {}"\
            .format(common_start_end_station[0], common_start_end_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (df) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum()
    print("Total travel time :", total_travel_duration)

    # display average travel time
    mean_travel_duration = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel_duration)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users
        Args:
        (df) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("The user types are:\n", user_counts)

    # display counts of gender
    
    if 'Gender' in df:
    # Only access Gender column in this case 
    gender_counts = df['Gender'].value_counts()
    print("\nThe gender types are:\n", gender_counts)
    else:
    print('Gender stats cannot be calculated because Gender does not appear in the data for the selected city')
    

    # display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:
    # Only access Birth Year column in this case 
        earliest_year_born = int(df['Birth Year'].min())
        print("\nThe oldest user is born of the year", earliest_year_born)
    
        recent_year_born = int(df['Birth Year'].max())
        print("The youngest user is born of the year", recent_year_born)
    
        common_year_born = int(df['Birth Year'].mode()[0])
        print("Most users are born of the year", common_year_born)
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the data for the selected city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_view(df):
    """Displays raw data based on user selection
        Args:
        (df) df - Pandas DataFrame containing city data filtered by month and day
    """
    counter = 0
    
    while True: 
        # gets user input, formats and validates
        raw_data = input('Want to see raw data for the city selected? \nEnter yes or no: ').lower().strip()
        if raw_data == 'yes': 
            # increment the counter and pull data using the counter as an index
            counter += 1 
            print(df.iloc[(counter-1)*5:counter*5])
        elif raw_data == 'no':
            return    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)        
        user_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
