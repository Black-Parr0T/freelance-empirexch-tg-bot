import random
import datetime
from csv import writer, reader
import string

indian_names = [
    "Aarav", "Priya", "Rajesh", "Vikram", "Suresh", "Deepak", "Ravi", "Anjali", "Amit", "Rina",
    "Kumar", "Singh", "Patel", "Mehta", "Sharma", "Yadav", "Khanna", "Desai", "Jain", "Iyer",
    "Chaudhary", "Vishnu", "Varma", "Prasad", "Nair", "Menon", "Raghavan", "Sundaram", "Khan", 
    "Das", "Singhvi", "Rathore", "Chopra", "Bose", "Mukherjee", "Kapoor", "Bhatt", "Reddy", 
    "Naidu", "Krishna", "Gopal", "Tiwari", "Chawla", "Ghosh", "Bhandari", "Rana", "Pillai", 
    "Thakur", "Bajpai", "Gupta", "Sen", "Rao", "Patwardhan", "Shukla", "Ishwar", "Lal", 
    "Vishal", "Nanda", "Khandelwal", "Dey", "Madhavan", "Sahani", "Lalwani", "Tiwari", 
    "Purohit", "Chandran", "Chitnis", "Mishra", "Rajput", "Joshi", "Yadav", "Bisht", 
    "Dhar", "Hegde", "Shetty", "Sharma", "Saini", "Kumaraswamy", "Saxena", "Tripathi", 
    "Ramaswamy", "Subramaniam", "Saraf", "Gandhi", "Khurana", "Bhaskar", "Modi", 
    "Chand", "Kapil", "Puneet", "Shivani", "Madhuri", "Amitabh", "Devendra", "Nishant", 
    "Lakshmi", "Jai", "Neelam", "Sonali", "Pooja", "Radhika", "Kriti", "Ayesha", 
    "Harsh", "Ishaan", "Asha", "Madhuri", "Bharati", "Rekha", "Vijay", "Krishna", 
    "Manish", "Siddharth", "Arvind", "Vivek", "Himanshu", "Sagar", "Pankaj", "Vandana", 
    "Rani", "Tarun", "Rupesh", "Vandana", "Arun", "Nisha", "Vijaya", "Maya", 
    "Ankit", "Sonal", "Chandni", "Chirag", "Chintu", "Harika", "Pritam", "Raghav", 
    "Ishwar", "Ankita", "Kriti", "Suraj", "Indira", "Suman", "Aaradhya", "Alok", 
    "Rajeev", "Yogesh", "Gaurav", "Sonia", "Divya", "Seema", "Tejas", "Ajay", 
    "Sushila", "Ajit", "Kavita", "Baba", "Mohan", "Maya", "Khushboo", "Tanu", 
    "Sheela", "Nidhi", "Priya", "Sahil", "Praveen", "Aarushi", "Sandeep", "Nitin", 
    "Sangeeta", "Jagdish", "Kavita", "Reena", "Lalita", "Abhishek", "Tanya", 
    "Neeraj", "Pooja", "Rita", "Bhavna", "Alok", "Rajni", "Ravi", "Ajay", 
    "Rani", "Ankit", "Shreya", "Rajendra", "Shivendra", "Amit", "Shruti", "Chandni", 
    "Manisha", "Ashok", "Tushar", "Rohit", "Sandeep", "Kunal", "Vandana", "Sandeep", 
    "Madhusree", "Sadhana", "Aarush", "Gaurav", "Bharti", "Swati", "Gagan", 
    "Charul", "Madhusree", "Sheela", "Shubham", "Chandan", "Shashi", "Suman", 
    "Bhawana", "Rakesh", "Kashish", "Usha", "Tushar", "Dev", "Mohan", "Vandana", 
    "Gurpreet", "Sangita", "Sanjay", "Ankita", "Sumit", "Gauri", "Inder", 
    "Chandrika", "Vishal", "Dinesh", "Jasmin", "Himanshu", "Monika", "Nikita", 
    "Jeevan", "Tanuja", "Sanjana", "Shashank", "Ishaan", "Rohini", "Vinay", 
    "Sundari", "Kunal", "Simran", "Preeti", "Ashish", "Vishnu", "Shruti", "Harish", 
    "Jagdish", "Swarnali", "Vasundhara", "Sumit", "Neelam", "Tanu", "Umesh", 
    "Rashmi", "Ravindra", "Ujjwal", "Devansh", "Priti", "Piyush", "Avinash", 
    "Sukhvinder", "Manoj", "Jyothi", "Nayan", "Sanjeev", "Meenal", "Hitesh", 
    "Geetanjali", "Mohini", "Payal", "Mansi", "Sumita", "Vidya", "Mahesh", 
    "Indira", "Madhavi", "Mithun", "Sunita", "Manohar", "Bhaskar", "Monika", 
    "Vikram", "Mahendra", "Shweta", "Kiran", "Balkrishna", "Punit", "Alok", 
    "Chandrika", "Meenakshi", "Amrita", "Naina", "Tarun", "Jaya", "Shilpa", 
    "Suman", "Dimple", "Vikram", "Raman", "Arun", "Rajiv", "Shubham", "Geeta", 
    "Khushbu", "Aarav", "Shashi", "Asha", "Devender", "Prema", "Suresh", 
    "Pramod", "Bhuvan", "Renu", "Rajeev", "Anju", "Dev", "Krishan", "Tejasvi", 
    "Gurinder", "Poonam", "Kiran", "Ravi", "Kartik", "Kavita", "Sandy", 
    "Shakuntala", "Umesh", "Rajeev", "Nandini", "Gitanjali", "Poonam", 
    "Nayan", "Mohit", "Avni", "Alok", "Rajinder", "Suman", "Anita", "Vijay", 
    "Yogita", "Anjali", "Laxmi", "Ravindra", "Suman", "Tanvi", "Gaurav", 
    "Nisha", "Poonam", "Vandana", "Madhvi", "Gauri", "Sarika", "Priti"
]
indian_surnames = [
    "Patel", "Sharma", "Singh", "Mehta", "Reddy", "Gupta", "Yadav", "Jain", "Iyer", "Rao",
    "Choudhury", "Kumar", "Shukla", "Chopra", "Nair", "Menon", "Khan", "Desai", "Bose", 
    "Mukherjee", "Kapoor", "Bhat", "Rathore", "Naidu", "Das", "Saxena", "Mishra", "Raghavan",
    "Bhandari", "Chandran", "Tiwari", "Varma", "Sundaram", "Bajaj", "Jadhav", "Ghosh", "Rana", 
    "Pillai", "Tripathi", "Khanna", "Rajput", "Vishnu", "Ahuja", "Bhaskar", "Gupta", "Bisht",
    "Saini", "Rao", "Bhatt", "Shetty", "Sen", "Madhavan", "Chitnis", "Vishal", "Purohit",
    "Rajeev", "Yogesh", "Raghuvanshi", "Rathi", "Panchal", "Lal", "Bansal", "Soni", "Chawla",
    "Chand", "Sood", "Bansal", "Khatri", "Agrawal", "Reddy", "Verma", "Khandelwal", "Suri", 
    "Agarwal", "Dey", "Modi", "Kaur", "Singhvi", "Nagpal", "Nandi", "Vohra", "Malik", "Dixit",
    "Bhatt", "Kohli", "Tiwari", "Jaiswal", "Shukla", "Panchal", "Bhatia", "Bawa", "Puri", 
    "Malhotra", "Kapoor", "Dhawan", "Agarwal", "Khurana", "Anand", "Tiwari", "Kumawat", 
    "Rastogi", "Sangwan", "Joshi", "Vyas", "Bhalla", "Pandey", "Ishwar", "Sood", "Gandhi",
    "Sharma", "Makhija", "Choudhary", "Sarkar", "Kochhar", "Rai", "Mittal", "Mohan", "Shukla",
    "Kapur", "Bhandari", "Das", "Gupta", "Sabharwal", "Saxena", "Sethi", "Goel", "Nagpal",
    "Sareen", "Khanna", "Mishra", "Ravindran", "Siddiqui", "Dagar", "Nanda", "Bedi", "Chawla"
]

def generate_username():

    first_name = random.choice(indian_names)
    last_name = random.choice(indian_surnames)

    first_name = first_name.lower()
    last_name = last_name.lower()
    
    digits = random.randint(100, 999)
    username = f"{first_name}{last_name}{digits}"
    return username

async def append_to_csv(file_path, data, header=None):
    file_exists = False
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    key_date = f"{file_path}_{today_date}"
    file_path = f"{key_date}.csv"
    try:
        with open(file_path, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_path, 'a', newline='') as file:
        csv_writer = writer(file)
        if not file_exists and header:
            csv_writer.writerow(header)
        csv_writer.writerow(data)

async def count_user_accounts(file_path,user_id,date=None):
    if not user_id:
        return 0, user_id
    count = 0
    try:
        if date:
            today_date = date
        else:
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        key_date = f"{file_path}_{today_date}"
        file_path = f"{key_date}.csv"
        with open(file_path, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if str(row[-2]) == str(user_id):
                    count += 1
        return count, user_id
    except Exception as e:
        print("Error: ", e)
        return count, user_id
    
async def count_campaign_code_accounts(file_path, campaign_code, date=None):
    if not campaign_code:
        return 0, campaign_code
    count = 0
    try:
        if date:
            today_date = date
        else:
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        key_date = f"{file_path}_{today_date}"
        file_path = f"{key_date}.csv"
        with open(file_path, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if row[-1] == campaign_code:
                    count += 1
        return count, campaign_code
    except Exception as e:
        print("Error: ", e)
        return count, campaign_code
    
async def total_registerations(file_path, date=None):
    if not file_path:
        return 0
    count = 0
    try:
        if date:
            today_date = date
        else:
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        key_date = f"{file_path}_{today_date}"
        file_path = f"{key_date}.csv"
        with open(file_path, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                count += 1
        return count
    except Exception as e:
        print("Error: ", e)
        return count
    
async def generate_random_string(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

async def match_data(data1, data2):
    return data1 == data2