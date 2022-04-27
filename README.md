## Building A Service Oriented Web Application - Digital Wallet System (eWallet) --> (POD A)

### For Context

The projects is:

Digital Wallet System (eWallet)

Project Overview<br>
eWallet is a type of pre-paid account in which a user can store his/her money for any future
online transaction. With the help of an E-wallet, one can make payments for groceries, online
purchases, and flight tickets, among others.

Project Specification/Instructions
1. This Project was done using Python as the base programming language.
2. Django REST Framework was used as the Server side Framework/API protocol for this project.
3. The Linting Library is Flake8.
4. The style Guide is PEP8.
5. The project centers on designing a wallet system for a product used in multiple countries.
6. The system would only be accessible to authenticated users.
7. There are three user types: Noob, Elite and Admin.

The following is the description of the three users that the app caters for:

1. THE NOOB:
i. can only have one wallet which automatically becomes their base currency. This base currency/wallet
will be selected upon registration and cannot be changed(by them);<br>
ii. since they cannot have more than one wallet, all transactions done by them is dependent on the base
currency. They can transact in other currencies but the debit or credit will always be added or
subtracted from the base currency.<br>
<br>
2. THE ELITE:
i. like the noob, can have only one base currency which will be selected upon registration and cannot
be changed(by them). Unlike the noob, however, they can have as many wallets as possible;<br>
ii. all credit transaction in any currency that does not yet exist in their wallet, creates a
new wallet for the elite user;<br>
iii. all debit transactions in a currency which wallet does not exist for the elite user will first be
converted to the base currency and then deducted from the base currency.<br>
<br>
3. THE ADMIN:
i. cannot have a wallet;<br>
ii. can fund users' accounts but cannot withdraw from the accounts;<br>
iii. can change the base currency of users - both noob an elite.<br>


Note: Dependencies are found in the Requirements.txt file.
