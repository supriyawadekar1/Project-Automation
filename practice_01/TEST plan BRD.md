║    TABLE OF CONTENTS      ║
I.	INTRODUCTION	1
1.1.	Module / Process Overview	1
1.2.	Abbreviations & Definitions	1
1.3.	Client Objective	1
1.4.	Scope of the Process	1
1.5.	Entry Criteria / Pre-requisites	2
1.6.	Exit CRITERIA / PRE-REQUISITES	2
II.	PROPOSED BUSINESS FLOW DIAGRAM	3
Proposed Business flow   description	4
III.	FUNCTIONAL DESCRIPTION	5
3.1.	Description of the Existing Client Process	5
3.2.	Description on the Limitations of the Existing Client Process	5
3.3.	Description of the Proposed System	6
3.4.	Constraints of the Proposed System	7
3.5.	Quality Criterion And Validations	7
3.6.	Use Cases	8
3.7.	Screen Designs	25
3.8.	Reports and Expected Outputs	25
3.9.	Error Messages and Conditions	25
3.10.	Volume / Data Analysis (Details of Present Data / Records)	25
3.11.	Performance Characteristics (User’s Basic Expectation)	25
3.12.	Criticality	25
IV.	DESIGN REQUIREMENTS	26
4.1.	User Usage	26
4.2.	Operating Environment – System Details	26
4.3.	Connectivity / Bandwidth / Localization Requirements	26
4.4.	Assumptions	26
4.5.	Dependencies	26
V.	IMPACT ANALYSIS	27
5.1.	Impact On Other Existing Application	27
5.2.	Impact On Other Existing Reports	27
VI.    EXTERNAL INTERFACE REQUIREMENTS	28
6.1.	User Intefaces or Requirements (UI)	28
6.2.	Hardware Interfaces or Requirements (HR)	28
6.3.	Software Interfaces Or Requirements (SR)	28
6.4.	Communications Interfaces (CI)	28
VII.   EXIT CRITERIA / POST FUNCTIONS	29
7.1.	Scalability / Performance / Response Time	29
7.2.	Security and Privacy	29
7.3.	Regulatory and Compliance Requirements	29
7.4.	Other Data Storage, Archival, Back-Up, Disaster Recovery	29
7.5.	Conclusion	29
VIII.	BRANDING GUIDELINES	30
8.1.	Shortcut Keys Standards	30
8.2.	Color Indexing Standards	30
IX.	BUSINESS CONTINUITY REQUIREMENTS	31
9.1.	Recovery Time Objective (RTO)	31
9.2.	Recovery Point Objective (RPO)	31
9.3.	Interdependencies	31
X.   WARRANTY PERIOD	31
XI.    LOAD DETAILS	32
11.1.	Recovery Time Objective (RTO)	32
11.2.	Application Unavailability	32
11.3.	Concurrent User Count	32
11.4.	Total User Count	32
11.5.	Applicable / Approved Downtime/ Maintenance Period	32
11.6.	Application Availability	32
XII.   APPENDIX / GLOSSARY	33
XIII.  ANNEXURE	33


 
I.	INTRODUCTION
1.1.	MODULE / PROCESS OVERVIEW
PO module 
Bot is a computer program that is designed to communicate with human users through the internet. It allows a form of interaction between a human and a machine the communication which happens via chat messages.
Chatbot for IT services needs to be developed to address all the basic IT queries of internal Mahindra users which will reduce the TAT for solving the self-help IT queries.
1.2.	ABBREVIATIONS & DEFINITIONS 
Terms	Meaning
MMFSL	Mahindra & Mahindra Financial Services Ltd.
HO	Head Office
	
	
	
	

1.3.	CLIENT OBJECTIVE  
Objectives of the client are as follows: 
•	To provide user support in solving the basic IT queries 
•	To provide solution 24/7
•	To provide solution to multiple users at the same time.
•	To increase the productivity of the work by reducing the time taken for the entire ticketing process.  
. 	 
1.4.	SCOPE OF THE PROCESS 
1.4.1.	In Scope
•	Creating Chatbot only for internal Mahindra users.
•	Self-help queries, FAQ’s , call tagging in felicity portal
•	Creating a bot flow for System related queries, Application queries, Insider Trading Compliance queries
•	Hosted as a website application
•	The Insider Trading Compliance application queries will be visible to authorized users. 
1.4.2.	Out of Scope


1.5.	ENTRY CRITERIA / PRE-REQUISITES

Entry criteria are the conditions that are required to begin the processing of the current stage

•	Requirements collection from internal Mahindra users, call reports
•	Analysis of requirements and documentation
•	Designing of structural bot flow document
•	Coding
•	Test Environment has been set up
•	Test cases/scripts are ready.

1.6.	EXIT CRITERIA / PRE-REQUISITES
The following requirements are to be checked before the project is deemed complete.
•	Requirements Analysis is complete when the Circle Head - IT signs off on the Functional Requirement document – bot flow document
•	Execution of all the high priority test cases
•	High risk identified area has been taken up and tested
•	Successfully deployed build in production with no high priority defects
•	Deadlines reached.
II.	PROPOSED BUSINESS FLOW DIAGRAM 
 
 Step	Description
Step 1	Open  MFBOT
Step 2	Select Type of Query for e g :System related,application etc 
Step 3	Select specific query among displayed options
Step 4	Solution will be displayed to the user for that particular query
Step 5	User gets a solution displayed on MFBOT Screen 
Step 6	User gets two options along with a solution as
1.was it helpful? Two checkboxes yes and NO
2.Do you want to Raise  a ticket?two checkboxes yes and NO
Step 7	On selecting yes for was it helpful menu user gets Thank you message
Step 8	If the user is not happy with the solution ticket can be raised
Step 9	To raise a ticket user need to enter SAP code and password,
Step 10	List of parameters required to raise a ticket will be displayed,user need to enter the details and information will be passed to the falicity portal
Step 11	MFBOT will display ticket number generated for the raised ticket for the user

III.	FUNCTIONAL DESCRIPTION
3.1.	DESCRIPTION OF THE EXISTING CLIENT PROCESS 
Following are the key features of the existing Client Process. 
•	Currently the PO processing is done manually. 
•	The respective authorities send an email to the purchase team for a new purchase request with available quotations if applicable. 
•	The request approval authority approves the request and assigns it to the PO team.
•	PO team processes the PO and initiates the approval process. 
•	After final approval the PO is sent to the vendor and the PO details are submitted to the payments team. 

3.2.	DESCRIPTION ON THE LIMITATIONS OF THE EXISTING CLIENT PROCESS
3.2.1.	Functional Issue 
Following are the functional limitations of the existing system: 
•	No detailed MIS or reports to track the branch wise expense. 
•	Asset details like model, serial number, configuration is not capturing in case of rental assets and AMC. 
•	Branch wise types of consumables and connectivity expenses are not getting tracked in the current system. 
•	Purchase requests are done manually or through mails which is time consuming. 
•	There is delay in releasing payments to vendors. 
•	There is no system to track VA. 

3.2.2.	Technology Issue 
3.2.3.	Framework Issue 
3.2.4.	Load Issue  
3.2.5.	Server Load Issue 
3.2.6.	Database Load Issue

3.3.	DESCRIPTION OF THE PROPOSED SYSTEM  

When a user opens MFBOT, welcome message will be displayed and asks to select the query from the list of categories as “please select from the following” for e.g if a user is facing an issue related to outlook software i,e if the user is unable to Configure Proxy Address in Outlook for Mahindra Mail id for Access the mail through Internet , the option that the user needs select will be system related,when the user selects the required option from the list. Next the user needs to select configure option,next the user needs to select proxy address for the Mahindra mail Id option, user will be displayed a solution for that particular query as 
Open Microsoft outlook , Go to Tools-->Account Setting-->Profile->Change--?More Setting-->Connection-->Select Connect to Microsoft Exchange using HTTP-->Select Exchange Proxy Server-->Enter Server Address " mfowa.mfeka.com " in Connection Setting-->Check the Box for Only Connect to Proxy Server....-->Enter Adders " msstd:mfowa.mfeka.com" --> Select the proxy Authentication Setting as " BASIC AUTHENTICATION" and Save ,with a message was it helpful? when the user respond back with yes, thank you message will be displayed if not, the user will be asked to raise a ticket in felicity portal, on successfully raising the ticket ticket number will be reverted back to the user on MFBOT screen.
3.4.	QUALITY CRITERION AND VALIDATIONS  


3.5.	SCREEN DESIGNS

 



 
3.6.	REPORTS AND EXPECTED OUTPUTS
A link of report for each of the selected PR devices should be displayed in the side of screen so that the user can view the reports w.r.t to the items present in the purchase request.  
3.7.	ERROR MESSAGES AND CONDITIONS 
3.8.	VOLUME / DATA ANALYSIS (DETAILS OF PRESENT DATA / RECORDS) 
3.9.	PERFORMANCE CHARACTERISTICS (USER’S BASIC EXPECTATION) 
3.10.	CRITICALITY

 

IV.	DESIGN REQUIREMENTS
4.1.	USER USAGE
4.1.1.	Total users expected to use the system (In first 3 / 6 / 12 months)

4.1.2.	What will be the storage space required

4.2.	OPERATING ENVIRONMENT – SYSTEM DETAILS
4.2.1.	Software
•	OS			:	
•	RDBMS		: 
•	Application	: 

4.2.2.	Hardware
•	Configuration	: 
•	RAM		: 
•	HDD		: 

4.3.	CONNECTIVITY / BANDWIDTH / LOCALIZATION REQUIREMENTS 
4.4.	ASSUMPTIONS 
4.5.	DEPENDENCIES

 

V.	IMPACT ANALYSIS
5.1.	IMPACT ON OTHER EXISTING APPLICATION
Requirement	Module	Impacted Application	Impacted Module	Functional Impact	Technical Impact	Criticality
(H/M/L)	Priority 
(H/M/L)
							
							
							

5.2.	IMPACT ON OTHER EXISTING REPORTS
Requirement	Module	Impacted Application	Impacted Report	Functional Impact	Technical Impact
					
					
					
 

VI.    EXTERNAL INTERFACE REQUIREMENTS
6.1.	USER INTEFACES OR REQUIREMENTS (UI)

6.2.	HARDWARE INTERFACES OR REQUIREMENTS (HR)

6.3.	SOFTWARE INTERFACES OR REQUIREMENTS (SR)

6.4.	COMMUNICATIONS INTERFACES (CI)


 

IX.	BUSINESS CONTINUITY REQUIREMENTS
9.1.	RECOVERY TIME OBJECTIVE (RTO) 
9.2.	RECOVERY POINT OBJECTIVE (RPO) 
9.3.	INTERDEPENDENCIES


X.   WARRANTY PERIOD

 

XI.    LOAD DETAILS
11.1.	RECOVERY TIME OBJECTIVE (RTO) 
11.2.	APPLICATION UNAVAILABILITY
Day	Period	Remarks (If any)
		
		
(Provide the server load details in peak hours / multiple peaks can be defined)

11.3.	CONCURRENT USER COUNT

11.4.	TOTAL USER COUNT

11.5.	APPLICABLE / APPROVED DOWNTIME/ MAINTENANCE PERIOD
Approved by	Specific Period
	
	

11.6.	APPLICATION AVAILABILITY
From Time	To Time	User Hits
		
		
		

 

