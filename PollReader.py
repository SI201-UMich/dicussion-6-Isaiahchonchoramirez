import os
import unittest

# We will be working with a dataset of 2024 US Presidential Election Polls
# ● The adapted dataset contains the following columns:
# ○ month - month of the year: 'aug' to 'sept’ – reminder: they are lower case
# ○ date - day of the month: integer representing the date of the month
# ○ sample - The number of people who responded to the poll and the type of respondents
# ■ A = Adults
# ■ V = Voters
# ■ LV = Likely Voters
# ■ RV = Registered Voters
# ○ Harris result - the percentage of respondents who preferred Harris
# ○ Trump result - the percentage of respondents who preferred Trump

# ● In the starter code you are given a class PollReader and several methods to implement
# ● PollReader reads in the CSV file and builds a dictionary where each key is the name of 
# a column, and each value is a list of the data in that column
# ● The dictionary is stored in an instance variable called data_dict
# becomes
# self.data_dict = {
#     ‘month’: [‘sept’, ‘sept’, ‘sept’...],
#     ‘date’: [19, 19, 17...],
#     ‘sample’: [1880, 1880, 810...],
#     ‘sample type’: [‘LV’, ‘LV’, ‘LV’...],
#     ‘Harris result’: [0.51, 0.53, 0.49...],
#     ‘Trump result’: [0.45, 0.47, 0.45...]
# }

# Your Task
# ● First, you’ll need to fix the bugs in the build_data_dict() method
# ○ HINT: Think about the header row and how columns are separated in CSVs
# ● Then you’ll need to implement each method of the PollReader class according to the instructions in 
# the starter code.
# ● We have provided several test cases for you that should pass if you’ve completed the assignment 
# successfully
# ● Please don’t change any of these test cases


class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        """
        Reads all of the raw data from the CSV and builds a dictionary where
        each key is the name of a column in the CSV, and each value is a list
        containing the data for each row under that column heading.

        There may be a couple bugs in this that you will need to fix.
        Remember that the first row of a CSV contains all of the column names,
        and each value in a CSV is seperated by a comma.
        """

        # iterate through each row of the data
        for i in self.raw_data[1:]: # skip the header row

            # split up the row by column
            seperated = i.split(',')

            # map each part of the row to the correct column
            self.data_dict['month'].append(seperated[0])
            self.data_dict['date'].append(int(seperated[1]))
            self.data_dict['sample'].append(int(seperated[2].split(" ")[0]))
            self.data_dict['sample type'].append(seperated[2].split(" ")[1])
            self.data_dict['Harris result'].append(float(seperated[3]))
            self.data_dict['Trump result'].append(float(seperated[4]))


    def highest_polling_candidate(self):
        """
        This method should iterate through the result columns and return
        the name of the candidate with the highest single polling percentage
        alongside the highest single polling percentage.
        If equal, return the highest single polling percentage and "EVEN".

        Returns:
            str: A string indicating the candidate with the highest polling percentage or EVEN,
             and the highest polling percentage.
        """
        
        highest_harris = max(self.data_dict['Harris result'])
        highest_trump = max(self.data_dict['Trump result'])
        if highest_harris > highest_trump:
            return f"Harris with {(highest_harris * 100):.1f}%"
        elif highest_trump > highest_harris:
            return f"Trump with {(highest_trump * 100):.1f}%"
        else:
            return f"EVEN with {(highest_harris * 100):.1f}%"  
        


    def likely_voter_polling_average(self):
        """
        Calculate the average polling percentage for each candidate among likely voters.

        Returns:
            tuple: A tuple containing the average polling percentages for Harris and Trump
                   among likely voters, in that order.
        """
        harris_total = 0
        trump_total = 0 
        count = 0
        likely_voter_indices = [i for i, sample_type in enumerate(self.data_dict['sample type']) if sample_type == 'LV']
        harris_total = sum(self.data_dict['Harris result'][i] for i in likely_voter_indices)
        trump_total = sum(self.data_dict['Trump result'][i] for i in likely_voter_indices)
        count = len(likely_voter_indices)
        harris_avg = harris_total / count if count > 0 else 0
        trump_avg = trump_total / count if count > 0 else 0
        return (harris_avg, trump_avg)

    def polling_history_change(self):
        """
        Calculate the change in polling averages between the earliest and latest polls.

        This method calculates the average result for each candidate in the earliest 30 polls
        and the latest 30 polls, then returns the net change.

        Returns:
            tuple: A tuple containing the net change for Harris and Trump, in that order.
                   Positive values indicate an increase, negative values indicate a decrease.
        """
        earliest_harris = sum(self.data_dict['Harris result'][:30]) / 30
        latest_harris = sum(self.data_dict['Harris result'][-30:]) / 30
        earliest_trump = sum(self.data_dict['Trump result'][:30]) / 30
        latest_trump = sum(self.data_dict['Trump result'][-30:]) / 30
        harris_change = latest_harris - earliest_harris
        trump_change = latest_trump - earliest_trump
        return (harris_change, trump_change)



class TestPollReader(unittest.TestCase):
    """
    Test cases for the PollReader class.
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")



if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)