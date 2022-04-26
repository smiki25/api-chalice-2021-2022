# Introduction 
Development of REST API and state server implementation for mobile application in order to view geographical objects in Bulgaria.
Building an automated process for implementing the platform in cloud infrastructure.
AWS Chalice is a serverless Python framework developed by Amazon. It shares so many similarities in syntax and semantics with Flask.
Like other serverless technology, Chalice allows the developer to be able to concentrate on application development
without having to deal with managing servers. It uses AWS Lambda and the Amazon API Gateway.
We will use Chalice to build a database REST API. Your users will be able to register accounts and add geographical objects.
Entries will be stored in a DynamoDB database. It is a NoSQL database system offered by Amazon. It stores data in the form of tables, items, and attributes.
# Getting Started


## Clone the project
*** 
```
$ git clone https://example.com
$ cd ../path/to/the/file
```

##Configure AWS Credentials
***
```
$ aws configure
```
You should get a prompt for the AWS Access Key ID, AWS Secret Access Key, default region name. Supply your AWS Access keys and a chosen region. You can use any available AWS region. Finally, you can skip the default output format to use the default option: None:
```
AWS Access Key ID [None]: ****************ABCD
AWS Secret Access Key [None]: ****************abCd
Default region name [None]: us-east-2
Default output format [None]:
```
Note: If you don't have AWS credentials yet, you will need to set up an IAM user 
##Set up Project Dependencies
Starting out, you will need to activate the virtual environment for your project.
```
python -m venv venv
```
Now, install the needed dependencies for the project from the requirements.txt. 
```
pip install -r requirements.txt
```

## Set up DynamoDB
First thing you need to install is docker.
```
https://www.docker.com/products/docker-desktop
```
After you are ready open a PowerShell prompt and write the Docker pull command.
```
docker pull amazon/dynamodb-local
```
Finally to execute the DynamoDB localy simply run.
```
docker run -p 8000:8000 amazon/dynamodb-local
```

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)