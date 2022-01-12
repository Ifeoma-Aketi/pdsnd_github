import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
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

  checker = True
  month_checker = True
  day_checker = True

  MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
  WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "all"]
  #get user input for city.
  while checker:
      city = input('I will like to get the city of your interest, 1: Chicago, 2: New york city, 3: Washington: ')
      city = city.lower()
      if city == '1' or city == 'chicago':
        print('Your city of interest is Chicago')
        city = 'chicago'
        checker = False
      elif city == '2' or city == 'new york city':
        print('Your city of interest is New york city')
        city = 'new york city'
        checker =  False
      elif city == '3' or city == 'washington':
        print('Your city of interest is Washington')
        city = 'washington'
        checker = False
      else:
        print('This input is not valid')
        checker = True

  #get user input for month.
  while month_checker:
      month = input('Choose a month between January to June or all for no filter: ').lower()
      if month in MONTHS:
        print(f'Your input is {month}')
        #month = month
        month_checker = False
      else:
        print('The month is not within the range given')
        month_checker = True

  #get user input for day.
  while day_checker:
      day = input('Choose a day out of the days of the week(from Monday to Sunday) or all for no filter: ').lower()
      if day in WEEKDAYS:
        print(f'Your input is {day}')
        day_checker = False
      else:
        print('check your day input, there is something wrong')
        day_checker = True

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

month_map = {1: 'january', 2:'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',}

week_map = { 0: 'monday', 1: 'tuesday', 2:  'wednesday', 3:  'thursday', 4:  'friday', 5:  'saturday', 6:  'sunday' }

      #print(type(city))
      df = pd.read_csv(city_data[city], index_col=[0])

      df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek.map(week_map)
      df['month'] = pd.to_datetime(df['Start Time']).dt.month.map(month_map)
      #print(df.head())

      if day != 'all':
        df = df[df['day_of_week'] == day]
      if month != 'all':
        df = df[df['month'] == month]
        df.drop('day_of_week',axis=1,inplace=True)
        df.drop('month',axis=1,inplace=True)

      return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print(df.head())
    df['month'] = (pd.to_datetime(df['Start Time']).dt.month).map(month_map)
    df['day_of_week'] = (pd.to_datetime(df['Start Time']).dt.dayofweek).map(week_map)
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    df = df[df['month'].notna()]
    df = df[df['day_of_week'].notna()]
    df = df[df['hour'].notna()]

    # display the most common month
    df['month'].mode()[0]

    # display the most common day of week
    df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'].mode()[0]

    most_common_month = df['month'].mode()[0]
    most_common_day = df['day_of_week'].mode()[0]
    most_common_hour = df ['hour'].mode()[0]

    print(f'The most common month is {most_common_month}')
    print(f'The most common day is {most_common_day}')
    print(f'The most common hour is {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_station_start  =  pd.DataFrame(df['Start Station'].value_counts(ascending = False)).index[0]
    print(f'The most common start station is {most_common_station_start}')

    # display most commonly used end station
    most_common_station_end  =  pd.DataFrame(df['End Station'].value_counts(ascending = False)).index[0]
    print(f'The most common end station is {most_common_station_end}')

    df['joint_station'] = df['Start Station'] + '/' + df['End Station']
    common_joint_stations = df['joint_station'].mode()[0]

    # display most frequent combination of start station and end station trip
    list_common_comb   = common_joint_stations.split('/')
    print(f'The most common Start Sation is :{list_common_comb[0]}, and End Station: {list_common_comb[1]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('  Trip Duration...')
    start_time = time.time()

    # display total travel time; cast to int, we don't need fractions of seconds!
    total_travel_time = int(df['Trip Duration'].sum())
    print('    Total travel time:   ', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('    Mean travel time:    ', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('  User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.DataFrame(df['User Type'].value_counts(), index=None)
    print(f'The user_type is: {user_types}')

    # 'Gender' and 'Birth Year' is only available for Chicago and New York City

    if 'Gender' in df.columns:
        #displays count of gender
        genders = df['Gender'].value_counts()
        for j in range(len(genders)):
            count = genders[j]
            gender = genders.index[j]
        print (f'The Gender count is : {gender}')
    else:
        print('There is no gender data in the source.')


    if 'Birth Year' in df.columns:
        print('\n What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
    else:
        print('No available birth date data.')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    """
    Ask user if they would like to see the datasets displayed in 5 rows.
    Ask if they will like to see 5 more rows.
    Ask till reply is no.
    """
    start_point = 5
    rows_start = 0
    rows_end = start_point - 1

    print()
    while True:
        row_data = input('will you like to see some row data? Enter yes or no ').lower()
        if row_data == 'yes':
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += start_point
            rows_end += start_point

            print('\n    Would you like to see the next {} rows?'.format(start_point))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
