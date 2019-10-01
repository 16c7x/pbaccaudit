# Purpose
A Bolt task to go out and retrieve user account data from a list of servers and then some Python code to search the returned data.
This has to scale to 2000+ servers with 500+ targeted accounts. 

# To run the job
If you have a Bolt server you can pull this down by adding the project to the **Puppetfile**.  
With a list of servers;
```
bolt task run pbaccaudit::getdata --nodes server1.example.com,server2.example.com --format=json > testdata.json
```
Or you can run with a text file listing servers, here I've used a file called server.list;
```
bolt task run pbaccaudit::getdata --nodes @server.list --format=json > testdata.json
```

# Contents of the json file
```
{ "items": [
{"node":"server1.example.com","status":"success","result":{"_output":",unix,linux,opsunix,opslinux,splunk"}}
,
{"node":"server2.example.com","status":"success","result":{"_output":",unix,linux,opsunix,opslinux,splunk"}}
,
{"node":"server3.example.com","status":"failure","result":{"_output":",unix,linux,opsunix,opslinux,splunk"}}
,
{"node":"server4.example.com","status":"success","result":{"_output":",unix,linux,opsunix,opslinux,splunk"}}
,
{"node":"server5.example.com","status":"success","result":{"_output":",unix,linux,opsunix,opslinux,splunk,bob"}}
],
"node_count": 5, "elapsed_time": 13 }

```

# Some better formatted output
```
{ 
   "items":[ 
      { 
         "node":"server1.example.com",
         "status":"success",
         "result":{ 
            "_output":",unix,linux,opsunix,opslinux,splunk"
         }
      },
      { 
         "node":"server2.example.com",
         "status":"success",
         "result":{ 
            "_output":",unix,linux,opsunix,opslinux,splunk"
         }
      },
      { 
         "node":"server3.example.com",
         "status":"failure",
         "result":{ 
            "_output":",unix,linux,opsunix,opslinux,splunk"
         }
      },
      { 
         "node":"server4.example.com",
         "status":"success",
         "result":{ 
            "_output":",unix,linux,opsunix,opslinux,splunk"
         }
      },
      { 
         "node":"server5.example.com",
         "status":"success",
         "result":{ 
            "_output":",unix,linux,opsunix,opslinux,splunk,bob"
         }
      }
   ],
   "node_count":5,
   "elapsed_time":13
}
```

# To extract data from the JSON file
To extract data from the JSON file use **accparse.py** this requires 3 inputs;
1. The output file name.
2. The operation, either search by account or by host.
3. The search string, the account name or host name.

Using a file that above here is an example of a search by host;
```
$ python accparse2.py -f output.json -s server4.example.com -o host
Gathering cmd line options
Searching output.json for server4.example.com by host

unix
linux
opsunix
opslinux
splunk
The following servers failed

```

And if you select a server that failed to respond to the Bolt task;
```
$ python accparse2.py -f output.json -s server3.example.com -o host
Gathering cmd line options
Searching output.json for server3.example.com by host
The following servers failed
server3.example.com
```
And here a search by account name;
```
$ python accparse2.py -f output.json -s linux -o account
Gathering cmd line options
Searching output.json for linux by account
server1.example.com
server2.example.com
server4.example.com
server5.example.com
The following servers failed
server3.example.com

```
Finaly, search an account name that does not exist;
```
$ python accparse2.py -f output.json -s nonbob -o account
Gathering cmd line options
Searching output.json for nonbob by account
The following servers failed
server3.example.com
```

