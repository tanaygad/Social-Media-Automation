1)Server Code:
The server code is deployed at render. To test the code one can use the website we have provided to test the working
each endpoint defined in the python server code.The code is deployed to so the client don't have to run the file locally
each time they want to  acess the website.

2)Instagram_PostAutomation_Code:
This node js code can be run after installing all the dependencies(using node install).To run the code start the express app and fetch the /get-info endpoint 
On running the code, if any post was scheduled on that day at that time then it will post it to instagram, otherwise it will return 'no doc found'
The output of this post automation can be seen on a testing account used by our team throughout the project named "dass2024club_team43"

3)Facebook_PostAutomation_Code:
This python code can be run after installing all the dependencies(using pip install). On running the code, if any post was
scheduled on that day at that time then it will post it to facebook, otherwise it will return 'no doc found'.
This uses a page_access_token linked to the user's account stored in a .env(to maintain privacy).For testing purposes our
team is using a dummy account's page_access_token which can be provided by us while evaluation if needed.

4)Database:
This python code can be run after installing all the dependencies(using pip install).On running the code it will add all 
the contents to our database.The database is directly used by our website so it is advised not to run the code since our client will start using this soon
and doing so would resret all data of all posts(scheduling,approving).

3)Webcrawler:
This python code can be run after installing all the dependencies(using pip install). This code can be run any time and is responsible
to add new products,items on the client's website to the database and create posts out of them regularly. This code ensures that
all the client's latest products and stories gets covered for posting puposes.